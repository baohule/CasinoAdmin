"""
@author: Kuro
"""
from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import Field, EmailStr, BaseModel
from uuid import UUID

from app.shared.schemas.ResponseSchemas import BaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel


class UserRecovery(CamelModel):
    """
    The UserRecovery class is a model that contains the information about a user's password recovery
    """

    email: EmailStr = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "test@test.com",
            }
        }


class Recovery(CamelModel):
    """
    The Recovery class is a model that represents a recovery
    """

    email: EmailStr
    code: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "this@that.com",
                "code": "434655",
                "password": "weakpassword",
            }
        }


class Response(BaseResponse):
    """
    The Response class is a model that represents a response to a question
    """

    error: Optional[str]
    response: Optional[str]
    success: Optional[bool]


class RecoveryResponse(BaseResponse):
    """
    The above class is a model that represents the response to a recovery request
    """

    error: Optional[str]
    success: Optional[bool]
    recovery_token: Optional[str]


class SMSStart(CamelModel):
    """
    SMSStart class is a model that represents the start of an SMS message
    """

    phone: str

    class Config:
        schema_extra = {
            "example": {
                "phone": "+14801234567",
            }
        }


# The EmailStart class is a model that contains the data fields for the start of an email
class EmailStart(CamelModel):
    email: str

    class Config:
        schema_extra = {
            "example": {
                "email": "this@that.com",
            }
        }


class SMSLogin(CamelModel):
    """
    SMSLogin class is a model that represents the start of an SMS message
    """

    phone: str
    code: str

    class Config:
        schema_extra = {"example": {"phone": "+14801234567", "code": "123456"}}


#
class EmailLogin(CamelModel):
    """
    The EmailLogin class is a model that represents a user's login credentials
    """

    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "this@that.com",
                "password": "123456",
            }
        }


# SMSStartRequest
class SMSStartResponse(BaseResponse):
    """
    A SMSStartResponse is a model that represents the response to a
    """

    response: Optional[UUID]
    phone_number: Optional[str]
    phone_verified: Optional[bool]
    request_language: Optional[str]
    error: Optional[str]


class EmailStartResponse(BaseResponse):
    """
    An email start response is a response to the start email verification endpoint
    """

    response: Optional[UUID]
    email: Optional[str]
    email_verified: Optional[bool]
    error: Optional[str]


class LoginResponse(CamelModel):
    # The OTPLoginResponse is a model that represents the response from the
    # OTP login endpoint
    access_token: Optional[str]
    refresh_token: Optional[str]
    # response: Optional[UUID]
    expires_in: Optional[int]
    token_type: Optional[str]
    # error: Optional[str]


#
#
class OIDLogin(CamelModel):
    """
    OIDLogin is a class that represents a user's login to the system
    """

    phone: Optional[str]
    email: Optional[str]
    code: str

    class Config:
        schema_extra = {
            "example": {
                "phone": "+14801234567",
                "email": "this@that.com",
                "code": "123456",
            }
        }


class OIDResponse(BaseResponse):
    """
    OIDResponse tells the Python interpreter that this class will be used
    to create objects that represent the OIDResponse JSON object in the API.
    """

    access_token: Optional[str]
    id_token: Optional[str]
    #
    error: Optional[str]


class RefreshTokenResponse(BaseResponse):
    """
    RefreshTokenResponse tells the API what to expect when it gets a response from the server.
    """

    access_token: Optional[str]
    success: bool
    error: Optional[str]


class CreateUserResponse(BaseResponse):
    response: Optional[LoginResponse]


class UserClaim(ORMCamelModel):
    """
    The UserClaim class is a model that represents a user's claim
    """

    id: Optional[UUID]
    email: Optional[str]
    username: Optional[str]
    phone: Optional[str]
    phoneNumber: Optional[str]
    admin: Optional[bool]
    agent: Optional[bool]
    expires: Optional[str]


class EmailLLoginResponse(BaseResponse):
    response: Optional[LoginResponse]


class EmailLoginResponse(BaseResponse):
    response: Optional[UserClaim]


class TokenDetail(ORMCamelModel):
    access_token: str
    user_claim: UserClaim


class TokenResponse(BaseResponse):
    success: bool
    response: Optional[TokenDetail]


class OTPLoginStart(CamelModel):
    phone_number: str = Field(example="+14801234567 - note the +1")

class OTPLoginVerify(CamelModel):
    phone_number: str
    code: str = Field(example="123456")

class LoginStartResponse(ORMCamelModel):
    message: Optional[str]
    phone_number: Optional[str]

class OTPLoginStartResponse(BaseResponse):
    response: Optional[LoginStartResponse]