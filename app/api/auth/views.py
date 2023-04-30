"""
@author: Kuro
"""
import logging

import pyotp
from pydantic import BaseModel

import settings
from app.api.admin.models import Admin
from app.api.agent.models import Agent
from app.api.auth.schema import UserClaim, OTPLoginStartResponse, OTPLoginStart, LoginStartResponse, OTPLoginVerify
from app.api.credit.models import Balance
from app.api.user import schema as user_schema
from app.api.user.models import User
from app.api.user.schema import AdminLogin, UserLogin, AgentLogin, AdminUserCreate, GeneratePassword, GeneratePasswordResponse, NewPassword
from app.shared.auth.auth_handler import sign_jwt, TokenResponse
from app.shared.auth.password_handler import get_password_hash
from typing import Union
from app.shared.auth.password_generator import generate_password
from app.shared.auth.token_handler import generate_confirmation_token, confirm_token
from app.shared.email.mailgun import send_password_email
from app.shared.twilio.sms import send_sms
from fastapi import APIRouter
from app.shared.schemas.ResponseSchemas import BaseResponse
from app.shared.twilio.templates.sms_templates import OTPStartMessage
# from app.shared.helper.logger import StandardizedLogger

# logger = StandardizedLogger(__name__)

from app import logger
logger.setLevel(logging.DEBUG)


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)
totp = pyotp.TOTP(settings.Config.otp_base, interval=60)

@router.post("/signup", response_model=TokenResponse)
async def create_user(context: AdminUserCreate) -> TokenResponse:
    """
    > Create a user and return a JWT if successful

    :param context: AdminUserCreate - This is the request body that is passed in
    :type context: AdminUserCreate
    :return: A TokenResponse
    """
    context_data = context.dict(exclude_unset=True)
    password_authentication = get_password_hash(context.password)
    context_data["password"] = password_authentication
    user_response = User.create(**context_data)
    if not user_response:
        return TokenResponse(success=False, error="Object not created")
    Balance.create(ownerId=user_response.id, balance=0)
    return sign_jwt(UserClaim(id=user_response.id, email=context.email))


def jwt_login(
    context: Union[AdminLogin, UserLogin, AgentLogin], admin=False, agent=False
) -> TokenResponse:
    """
    Takes a context object, which is either an AdminLogin, UserLogin or AgentLogin,
    and returns a signed JWT if the password is correct, otherwise it returns a
    BaseResponse with an error message

    :param context: Union[AdminLogin, UserLogin, AgentLogin]
    :type context: Union[AdminLogin, UserLogin, AgentLogin]
    :param admin: Boolean, if True, the user is an admin, defaults to False (optional)
    :param agent: bool = False, defaults to False (optional)
    :return: A signed JWT token
    """
    model = admin and Admin or agent and Agent or User
    claim: UserClaim = model.user_claims(**context.dict())
    if not claim:
        return TokenResponse(success=False, error="Wrong login details")
    try:
        claim.admin = admin
        claim.agent = agent
    except Exception as e:
        model.session.rollback()
        print(e)
    signed_jwt: TokenResponse = sign_jwt(claim)
    return signed_jwt


@router.post("/login/agent", response_model=TokenResponse)
async def agent_login(context: AgentLogin) -> TokenResponse:
    """
    This function logs in an agent and returns a token response using JWT authentication.

    :param context: The `context` parameter in the `agent_login` function is an instance of the
    `AgentLogin` class. It likely contains information about the agent trying to log in,
    such as their name and password
    :type context: AgentLogin
    :return: The function `agent_login` is returning a
    `TokenResponse` object. The `TokenResponse` object
    is the result of calling the `jwt_login` function with the
    `context` argument
    and the `agent` parameter set to `True`.
    """
    return jwt_login(context, agent=True)


@router.post("/login/admin", response_model=TokenResponse)
async def admin_login(context: AdminLogin) -> TokenResponse:
    """
    This function logs in an agent and returns a dictionary with a JWT token.

    :param context: The context parameter is an instance of the
    AgentLogin schema class, which is used to pass in the user object. This object contains
     information about the user who
    is attempting to log in, such as their email and password
    :type context: AgentLogin
    :return: a dictionary with a JWT token.
    """
    return jwt_login(context, admin=True)


@router.post("/login/user", response_model=TokenResponse)
async def email_login(context: UserLogin) -> TokenResponse:
    """
    Takes a user login object, and returns a token response
    :param context: UserLogin
    :return: A token response
    """
    return jwt_login(context)


@router.post("/generate_password", response_model=GeneratePasswordResponse)
async def generate_random_password(context: GeneratePassword):
    """
    This function generates a new password for a user, hashes it, updates the user's
    password in the database, sends an email with the new password, and returns a response
    indicating success or failure.

    :param context: The context parameter is an instance of the GeneratePassword class,
    which likely contains id for the user for whom the password is being generated,
    :type context: GeneratePassword
    :return: The function `generate_password` returns either a `GeneratePasswordResponse`
    object with a `success` flag set to `True`, a `response` field containing a `NewPassword`
    object with the newly generated password, and no error message, or a `BaseResponse`
    object with a `success` flag set to `False` and an error message.
    """
    new_password = generate_password()
    hash_password = get_password_hash(new_password)
    if user := User.update_user(id=context.id, password=hash_password):
        send_password_email(user.email, User.username, new_password)
        return GeneratePasswordResponse(success=True, response=NewPassword(password=new_password))
    return BaseResponse(success=False, error="Email Not Sent")


@router.post("/login/otp/start", response_model=OTPLoginStartResponse)
async def start_otp_login(context: OTPLoginStart):
    """
    This function initiates the OTP login process by generating an OTP, storing it in the database,
    and sending it to the user's email address.

    :param context: The context parameter is an instance of the OTPLoginStart class, which
    likely contains the user's email address
    :type context: OTPLoginStart
    :return: The function `start_otp_login` returns a `OTPLoginStartResponse` object with a
    `success` flag set to `True` and no error message.
    """
    phone_list = User.session.query(User.phone).filter_by(active=False).all()
    disabled_list = [phone[0] for phone in phone_list if phone[0]]
    if context.phone_number in disabled_list:
        return BaseResponse(success=False, error="User is disabled please contact the user Agent")

    otp = totp.now()
    otp_response = OTPStartMessage(otp=otp)
    # sms_sent = send_sms(context.phone_number, otp_response.message)
    #
    # if not sms_sent:
    #     return BaseResponse(success=False, error="OTP not sent")

    response = LoginStartResponse(
        message=f"OTP sent to your phone number {otp}",
        phone_number=context.phone_number

    )
    return OTPLoginStartResponse(success=True, response=response)


class AttemptedLogin:
    """
    This class is used to keep track of the number of times a user has attempted to log in
    follows singleton pattern
    """
    _instance = None
    attempts = 0

    def __init__(self, phone_number: str):
        self.phone_number = phone_number
        self.attempts = self.attempts

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


@router.post("/login/otp/verify", response_model=TokenResponse)
async def verify_otp_login(context: OTPLoginVerify):
    """
    This function verifies an OTP and returns a JWT token if the OTP is correct.

    :param context: The context parameter is an instance of the OTPLoginVerify class,
    which likely contains the user's email address and the OTP they entered
    :type context: OTPLoginVerify
    :return: The function `verify_otp_login` returns either a `OTPLoginVerifyResponse`
    object with a `success` flag set to `True`, a `response` field containing a
    `TokenResponse` object with a JWT token, and no error message, or a `BaseResponse`
    object with a `success` flag set to `False` and an error message.
    """
    otp_logins = AttemptedLogin(phone_number=context.phone_number)
    phone_list = User.session.query(User.phone).filter_by(active=False).all()
    disabled_list = [phone[0] for phone in phone_list if phone[0]]

    if context.phone_number in disabled_list:
        return BaseResponse(success=False, error="User Disabled, Please Contact user Agent")
    if totp.verify(context.code):

        if user := User.read(phone=context.phone_number):
            response: TokenResponse = sign_jwt(
                UserClaim(
                    id=user.id,
                    email=user.email,
                    phone=user.phone,
                    username=user.username
                )
            )
            User.update(
                id=user.id,
                accessToken=response.response.access_token
            )
            return response
        return BaseResponse(success=False, error="User not found")

    otp_logins.attempts += 1
    if otp_logins.attempts == 3:
        if user := User.read(phone=context.phone_number):
            logger.info(f"Deactivating user {context.phone_number} for too many failed attempts")
            user.active = False
            user.session.commit()
            otp_logins.attempts = 0
            return BaseResponse(success=False, error="Phone Disabled for too many attempts")

    if otp_logins.attempts >= 3:
        return BaseResponse(success=False, error="Phone Disabled for too many attempts")

    return BaseResponse(success=False, error="OTP not verified")