from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
import re

from fastapi_camelcase import CamelModel
from pydantic import EmailStr, validator

from app.shared.schemas.ResponseSchemas import BaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel

from typing import Optional
from pydantic import BaseModel


class AdminRoleCreate(CamelModel):
    """
    Pydantic model to represent the request payload for creating a new admin role.
    """
    name: str
    parameters: dict
    bypass_auth: Optional[bool] = False


class AdminRoleCreateResponse(ORMCamelModel):
    """
    Pydantic model to represent the response payload for creating a new admin role.
    """
    success: bool
    error: Optional[str]
    role_id: Optional[str]


class AdminUserCreate(CamelModel):
    """
    `UserCreate` is a class that is used to validate the data that is being passed to the `/user` route.
    """

    email: EmailStr
    password: str
    name: str

    class Config:
        schema_extra = {
            "example": {
                "email": "some@example.com",
                "password": "adfgszfgsdgsfghsfg",
                "name": "some guy",
            },
            "Valid Phone Numbers": [
                "+14063335555 OR 406335555",
                "+14063335555",
                "+1 (406) 333-5555",
            ],
        }


class UserLogin(CamelModel):
    """
    A class that is used to validate the data that is being passed to the `/login` route.

    """

    phone: str

    class Config:
        schema_extra = {
            "example": {
                "phone": "+19164200014",
            }
        }


class AdminLogin(CamelModel):
    """
    This is a class that is used to validate the data that is being passed to the `/admin/login` route.

    """

    email: str
    password: str

    class Config:
        schema_extra = {"example": {"email": "test@test.com", "password": "1234567"}}


class UserResponse(BaseResponse):
    """
    `UserResponse` is a class that is used to validate the data that is being passed to the `/login` route.
    """

    error: Optional[str]
    response: Optional[str]
    success: Optional[bool]
    access_token: Optional[str]
    refresh_token: Optional[str]


class GetUser(CamelModel):
    """
    `GetUser` is a class that is used to validate the data that is being passed to the `/user/{userId}` route.
    """

    user_id: UUID

    class Config:
        schema_extra = {
            "example": {
                "userId": "eb773795-b3a2-4d0e-af1d-4b1c9d90ae26",
            }
        }


class AdminBaseResponse(ORMCamelModel):
    """
    `UserBaseResponse` is a class that is used to validate the data that is being passed to the `/user/{userId}` route.

    """

    success: bool
    error: Optional[str]
    response: Optional[UUID]
    name: Optional[str]
    username: Optional[str]
    created_at: Optional[datetime]
    response: Optional[UUID]


class AdminUpdateName(CamelModel):
    """
    This is a class that is used to validate the data that is being passed to the `/user/{userId}/update/name` route.

    """

    name: str


class AdminUpdateNameResponse(BaseResponse):
    """
    A class that is used to validate the data that is being passed to the `/user/{userId}/update/name` route.

    """

    success: bool
    error: Optional[str]


class CLaimAuthPayload(CamelModel):
    """
    This class is used to claim a user's account
    """

    user_id: UUID
    user_email: str
