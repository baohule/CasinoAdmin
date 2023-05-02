"""
@author: Kuro
"""
from enum import Enum

from app import logging
from datetime import datetime, timedelta

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

logger = logging.getLogger("auth")
logger.addHandler(logging.StreamHandler())
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
    logger.info(f"Attempting to login {context.email}")
    model = admin and Admin or agent and Agent or User
    logger.info(f"Model selected is {model}")
    claim: UserClaim = model.user_claims(**context.dict())
    logger.info(f"Claim is {claim}")
    if not claim:
        logger.info("No claim found")
        return TokenResponse(success=False, error="Wrong login details")
    try:
        claim.admin = admin
        claim.agent = agent
    except Exception as e:
        model.session.rollback()
        logger.error(str(e))
    signed_jwt: TokenResponse = sign_jwt(claim)
    logger.info(f"Signed JWT is {signed_jwt.response.access_token}")
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


class AttemptedLogin:
    """
    This class is used to keep track of the number of times a user has attempted to log in
    follows singleton pattern
    """
    _instance = None
    phone_number = None
    verify_attempts = 0
    send_attempts = 0
    last_attempt = datetime.now() - timedelta(minutes=1)

    def __init__(self, phone_number: str):
        self.phone_number = phone_number
        self.verify_attempts = self.verify_attempts
        self.send_attempts = self.send_attempts
        self.last_attempt = self.last_attempt

    def __new__(cls, *args, **kwargs):
        if cls.phone_number != kwargs.get("phone_number"):
            cls._instance = super().__new__(cls)
        return cls._instance


class OTPError:
    _instance = None
    time_left = ""
    NotVerified = "OTP not verified"
    Expired = "OTP expired"
    Invalid = "Invalid OTP"
    MaxAttempts = "Phone disabled for maximum attempts reached"
    NotSent = "OTP not sent"
    NotStarted = "OTP not started"
    UserDisabled = "User is disabled please contact the admin"
    UserNotFound = "User not found"
    TooManyRequests = f""
    DeactivatingUser = f""

    def __init__(self, time_left: timedelta = None, phone_number: str = None):
        self.time_left = time_left
        self.TooManyRequests = f"Too many requests please try again in {time_left} seconds"
        self.DeactivatingUser = f"Deactivating user {phone_number} for too many failed attempts"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


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
    phone_list = User.session.query(User.phoneNumber).filter_by(active=False).all()
    disabled_list = [phone[0] for phone in phone_list if phone[0]]
    if context.phone_number in disabled_list:
        return BaseResponse(success=False, error=OTPError.UserDisabled)
    otp_logins = AttemptedLogin(phone_number=context.phone_number)
    if (
            otp_logins.send_attempts >= 3
            and otp_logins.last_attempt + timedelta(hours=1) < datetime.now()
    ):
        otp_logins.send_attempts = 0

    delta = otp_logins.last_attempt + timedelta(minutes=1)
    if delta > datetime.now() or otp_logins.send_attempts >= 3:
        error = OTPError(time_left=delta - datetime.now() if otp_logins.send_attempts < 3 else (otp_logins.last_attempt + timedelta(hours=1)) - datetime.now())
        return BaseResponse(success=False, error=error.TooManyRequests)
    otp = totp.now()
    otp_response = OTPStartMessage(otp=otp)
    sms_sent = send_sms(context.phone_number, otp_response.message)
    otp_logins.send_attempts += 1
    otp_logins.last_attempt = datetime.now()
    if not sms_sent:
        return BaseResponse(success=False, error=OTPError.NotSent)
    otp_non_debug = 'OTP sent to your phone number'
    otp_debug = f"DEBUG: {otp_response.message}"
    response = LoginStartResponse(
        message=otp_debug,
        phone_number=context.phone_number,
    )
    logger.info(response.message)
    return OTPLoginStartResponse(success=True, response=response)


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
    logger.info(f"Verifying OTP for {context.phone_number} with code {context.code}")
    otp_logins = AttemptedLogin(phone_number=context.phone_number)
    phone_list = User.session.query(User.phoneNumber).filter_by(active=False).all()
    disabled_list = [phone[0] for phone in phone_list if phone[0]]

    if context.phone_number in disabled_list:
        return BaseResponse(success=False, error=OTPError.UserDisabled)
    if totp.verify(context.code):
        otp_logins.verify_attempts = 0
        logger.info("OTP verified, looking up user")
        if user := User.read(phoneNumber=context.phone_number):
            logger.info(f"User {user.id} found, generating JWT")
            response: TokenResponse = sign_jwt(
                UserClaim(
                    id=user.id,
                    email=user.email,
                    phoneNumber=user.phoneNumber,
                    username=user.username
                )
            )
            User.update(
                id=user.id,
                accessToken=response.response.access_token
            )
            return response
        return BaseResponse(success=False, error=OTPError.UserNotFound)

    otp_logins.verify_attempts += 1
    if otp_logins.verify_attempts == 3:
        if user := User.read(phoneNumber=context.phone_number):
            error = OTPError(phone_number=context.phone_number)
            logger.info(error.DeactivatingUser)
            user.active = False
            user.session.commit()
            otp_logins.verify_attempts = 0
            return BaseResponse(success=False, error=error.DeactivatingUser)

    if otp_logins.verify_attempts >= 3:
        return BaseResponse(success=False, error=OTPError.UserDisabled)

    return BaseResponse(success=False, error=OTPError.NotVerified)
