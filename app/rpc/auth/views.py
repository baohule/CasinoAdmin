"""
@author: igor
"""
import json
import logging

from py_linq import Enumerable


from app.api.auth.schema import OTPLoginStart, OTPLoginVerify, TokenResponse, OTPLoginStartResponse
from app.api.auth.views import start_otp_login, verify_otp_login
from app.api.user.models import User
from app.rpc.user.schema import User as UserSchema
from app.rpc.user.schema import UserResponse
from app.rpc.game.schema import Session, SocketSession
from app.shared.middleware.json_encoders import ModelEncoder
from app.rpc import socket

logger = logging.getLogger("auth")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

default_session = {
    'sid': None,
    'state': None
}


@socket.on('getOTP')
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
    socket_session = await socket.get_session(socket_id)
    if not socket_session:
        socket_session = SocketSession.construct(**{context.phoneNumber: default_session})
        logger.info(f'session: {socket_session}')

    session = Session(**socket_session.dict().get(context.phoneNumber))
    if session.state != 'sms_wait':
        response: OTPLoginStartResponse = await start_otp_login(context)
        session.sid = socket_id
        session.state = 'sms_wait'
        socket_session = socket_session.update_session(session)
        await socket.save_session(socket_id, socket_session.dict())
        await socket.emit("getOTP", data=response.dict())
    return OTPLoginStartResponse(success=False, error="SMS already sent")


@socket.on('verifySMS')
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
    socket_session = SocketSession.construct(**await socket.get_session(socket_id))
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
        await socket.save_session(socket_id, socket_session.dict())

    await socket.emit('loginResult', result.dict())
    return TokenResponse(success=False, error="SMS not sent")


async def update_online_users(user, online=True):
    """
    This function updates the online status of a user, retrieves a list of online users, logs the list, stores the list in Redis, and returns the list.

    :param user: The "user" parameter is an instance of a user model object that represents a user in the system. It is used to update the user's online status and retrieve a list of
    all online users
    :param online: The "online" parameter is a boolean value that indicates whether the user is currently online or not. If it is set to True, it means the user is online, and if it is
    set to False, it means the user is offline. The function updates the "online" attribute of the user, defaults to True (optional)
    :return: a list of online users, which are instances of the `UserSchema` class.
    """
    user.update(**dict(online=online))
    user.session.commit()
    online_users = [json.dumps(UserSchema.from_orm(user).dict(), cls=ModelEncoder) for user in User.read_all(online=True)]
    logger.info(f"online users: {online_users}")
    await redis.set('online_users', json.dumps(online_users, cls=ModelEncoder))
    return online_users


def get_auth_token(socket):
    """
    This function retrieves the authorization token from a socket object.

    :param socket: The `socket` parameter is an object representing a WebSocket connection. It is likely an instance of the `SocketIO` class from the `socketio` library in Python
    :return: The function `get_auth_token` returns the authentication token from the `HTTP_AUTHORIZATION` header of the socket's environment. The token is extracted from the header by
    splitting the header string at the space character and returning the second element of the resulting list.
    """
    return Enumerable(
        socket.environ.values()
    ).select(
        lambda x: x['HTTP_AUTHORIZATION']
    ).first().split(' ')[1]


@socket.on('login')
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
    logger.info('login')
    socket.emit('loginResult', 'login')
    token = get_auth_token(socket)
    socket_session = SocketSession.construct(**await socket.get_session(socket_id))
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
        socket_session = SocketSession.construct(socket.session(socket_id))
        response = UserResponse(success=True, response=user)
        session = Session(sid=socket_id, user=user, state='login_success')
        socket_session = socket_session.dict()
        socket_session[user.phoneNumber] = session.json()
        logger.info(socket_session)
        await update_online_users(user)
        await socket.save_session(socket_id, socket_session)
        await socket.emit('loginResult', response.json())

        return response


@socket.on('logout')
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
    token = get_auth_token(socket)

    user = User.where(accessToken=token).first()
    await update_online_users(user, online=False)
    user.accessToken = None
    user.save()
    await socket.emit('logoutResult', user.id)
    return
