"""
@author: igor
"""
import json
import logging
from types import SimpleNamespace
from typing import Dict, List

from app.api.auth.views import start_otp_login, verify_otp_login

from app.api.auth.schema import OTPLoginStart, OTPLoginVerify, TokenResponse, OTPLoginStartResponse
from app.api.game.models import PlayerSession
from app.api.user.models import User
from app.rpc.auth.schema import AccesToken, RedisUsers
from app.rpc.user.schema import UserLogin, UserResponse, UserSession
from app.rpc.user.schema import User as UserSchema
from fastapi import APIRouter

import uuid
from app import main_socket
from app.shared.helper.session_state import SocketSession, Session
from app.shared.middleware.json_encoders import ModelEncoder
from app.shared.redis.redis_services import RedisServices
from py_linq import Enumerable

logger = logging.getLogger("auth")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

default_session = {
    'sid': None,
    'state': None
}

redis = RedisServices().redis


@main_socket.on('getOTP')
async def get_OTP(socket_id, context: OTPLoginStart) -> OTPLoginStartResponse:
    """
    This function gets an OTP for login and emits it through a socket.

    :param socket_id:
    :param context: The parameter `context` is of type `OTPLoginStart`, which
    is likely a data class or a dictionary containing information required
     to start the OTP login process. The exact
    contents of this data class or dictionary would depend on the specific
    implementation of the `start_otp_login` function
    :return: The function `get_OTP` is returning an instance of
    `OTPLoginStartResponse`.
    """
    context = OTPLoginStart(**context)
    socket_session = await main_socket.get_session(socket_id)
    if not socket_session:
        socket_session = SocketSession.construct(**{context.phoneNumber: default_session})
        logger.info(f'session: {socket_session}')

    session = Session(**socket_session.dict().get(context.phoneNumber))
    if session.state != 'sms_wait':
        response: OTPLoginStartResponse = await start_otp_login(context)
        session.sid = socket_id
        session.state = 'sms_wait'
        socket_session = socket_session.update_session(session)
        await main_socket.save_session(socket_id, socket_session.dict())
        await main_socket.emit("getOTP", data=response.dict())
    return OTPLoginStartResponse(success=False, error="SMS already sent")


@main_socket.on('verifySMS')
async def verify_SMS(socket_id, context: OTPLoginVerify) -> TokenResponse:
    """
    The function verifies a user's login using a one-time password
    and emits the result through a socket.

    :param socket_id:
    :param context: The parameter "context" is of type OTPLoginVerify,
    which is likely a data class or a dictionary containing information
    related to a user's login attempt using a one-time
    password (OTP). This information may include the user's phone number,
    the OTP code, and any other relevant details needed to verify
    :return: a variable named "result" which is of type TokenResponse.
    """
    context = OTPLoginVerify(**context)
    socket_session = SocketSession.construct(**await main_socket.get_session(socket_id))
    session = Session(**socket_session.dict().get(context.phoneNumber))
    result = TokenResponse(success=False, error="SMS not sent")
    logger.info(f'session: {session}')
    if session.state == 'sms_wait':
        result: TokenResponse = await verify_otp_login(context)

        if result.success:
            session.state = 'login_success'
            session.user = UserSchema(**result.response.user_claim.dict())
            session.user.accessToken = result.response.access_token
            user = User.read(id=session.user.id)
            await update_online_users(user)

        if not result.success:
            session.state = 'login_failure'

        socket_session = socket_session.update_session(session)
        await main_socket.save_session(socket_id, socket_session.dict())

    await main_socket.emit('loginResult', result.dict())
    return TokenResponse(success=False, error="SMS not sent")


async def update_online_users(user, online=True):
    user.update(**dict(online=online))
    user.session.commit()
    online_users = [json.dumps(UserSchema.from_orm(user.to_dict(nested=True)), cls=ModelEncoder) for user in User.read_all(online=True)]
    logger.info(f"online users: {online_users}")
    await redis.set('online_users', json.dumps(online_users, cls=ModelEncoder))
    return online_users


def get_auth_token(socket):
    return Enumerable(
        socket._sio.environ.values()
    ).select(
        lambda x: x['HTTP_AUTHORIZATION']
    ).first().split(' ')[1]


@main_socket.on('login')
async def log_in(socket_id, _context) -> UserResponse:
    """
    The function logs in a user by checking their access token
    and returning a response object.

    :param context: The parameter `data` is of type `UserLogin`,
    which is likely a data class or a dictionary containing information
    required for user authentication, such as an access
    token
    :return: a `BaseResponse` object.
    """

    token = get_auth_token(main_socket)
    socket_session = SocketSession.construct(**await main_socket.get_session(socket_id))
    user = None
    if token:
        user = User.read(accessToken=token)
        logger.info(f'user: {json.dumps(user.to_dict(), cls=ModelEncoder)}')

    for session in socket_session.dict().values():
        if access_token := session['user'].get('accessToken'):
            user = User.read(accessToken=access_token)
            logger.info(f'user: {user} - {socket_session}')
            break

    if user:
        socket_session = SocketSession.construct(main_socket.session(socket_id))
        response = UserResponse(success=True, response=user)
        session = Session(sid=socket_id, user=user, state='login_success')
        socket_session = socket_session.dict()
        socket_session[user.phoneNumber] = session.json()
        logger.info(socket_session)
        await update_online_users(user)
        await main_socket.save_session(socket_id, socket_session)
        await main_socket.emit('loginResult', response.json())

        return response


@main_socket.on('logout')
async def log_out(socket_id):
    """
    The function logs out a user by setting their access token to None.

    :param accessToken: The `accessToken` parameter is a string that represents a
    unique token that is used to authenticate and authorize a user's access to a
    system or application. In
    this code snippet, the `accessToken` is used to identify the user who wants to
     log out and revoke their access token by setting it to `
    :type accessToken: str
    :return: Nothing is being returned explicitly in this function. The function simply updates the access token of a user to None and saves the changes to the database.
    """
    token = get_auth_token(main_socket)

    user = User.where(accessToken=token).first()
    await update_online_users(user, online=False)
    user.accessToken = None
    user.save()
    await main_socket.emit('logoutResult', user.id)
    return
