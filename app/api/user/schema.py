"""
@author: Kuro
"""
from datetime import date, datetime
from typing import Optional, List, Union
from uuid import UUID
import re

from fastapi_camelcase import CamelModel
from pydantic import EmailStr, validator, Field

from app.api.auth.schema import TokenDetail, TokenResponse
from app.shared.schemas.ResponseSchemas import BaseResponse, PagedBaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel

from typing import Optional
from pydantic import BaseModel

from app.shared.schemas.page_schema import GetPages, PagedResponse


class UserCredit(ORMCamelModel):
    balance: Optional[float]
    updatedAt: Optional[datetime]





class User(ORMCamelModel):
    id: Optional[UUID]
    email: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    balance: Optional[UserCredit] = Field(default=UserCredit(balance=0))
    username: Optional[str]
    createdAt: Optional[datetime]
    active: Optional[bool]


class BaseUser(ORMCamelModel):
    """
    `User` is a class that is used to validate the data that is being passed to the `/user` route.
    """

    id: Optional[UUID]
    email: Optional[str]
    username: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    creditAccount: Optional[UserCredit]
    active: Optional[bool]


class LoadUserResponse(BaseResponse):
    """
    `LoadUserResponse` is a class that is used to validate the data that is being passed to the `/user` route.
    """

    response: Optional[BaseUser]


class AgentUserCreateResponse(BaseResponse):
    """
    `UserCreateResponse` is a class that is used to validate the data that is being passed to the `/user` route.
    """

    success: bool = Field(default=False)
    response: Optional[Union[BaseUser, TokenDetail]]


class AdminUserCreateResponse(TokenResponse):
    """
    `AdminUserCreateResponse` is a class that is used to validate the data that is being passed to the `/user` route.
    """

    success: bool = Field(default=False)
    response: Optional[Union[BaseUser, TokenDetail]]


class AdminUserCreate(CamelModel):
    """
    `UserCreate` is a class that is used to validate the data that is being passed to the `/user` route.
    """

    email: EmailStr
    password: str
    username: str



class AgentUserCreate(CamelModel):
    """
    `UserCreate` is a class that is used to validate the data that is being passed to the `/user` route.
    """

    email: EmailStr
    password: str
    quota: Optional[int]



class UserLogin(CamelModel):
    """
    A class that is used to validate the data that is being passed to the `/login` route.
    """

    email: EmailStr
    password: str


class AdminLogin(CamelModel):
    """
    This is a class that is used to validate the data that is being passed to the `/admin/login` route.

    """

    email: str
    password: str

    class Config:
        schema_extra = {"example": {"email": "test@test.com", "password": "1234567"}}


class AgentLogin(CamelModel):
    """
    This is a class that is used to validate the data that is being passed to the route.

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
    response: Optional[AdminUserCreate]
    success: Optional[bool]


class GetUser(CamelModel):
    """
    `GetUser` is a class that is used to validate the data that is being passed to the `/user/{userId}` route.
    """

    id: UUID


class AdminBaseResponse(ORMCamelModel):
    """
    `UserBaseResponse` is a class that is used to validate the data that is being passed to the `/user/{userId}` route.

    """

    success: bool
    error: Optional[str]
    response: Optional[UUID]
    username: Optional[str]
    username: Optional[str]
    createdAt: Optional[datetime]
    response: Optional[UUID]


class AdminUpdateName(CamelModel):
    """
    This is a class that is used to validate the data that is being passed to the `/user/{userId}/update/name` route.

    """

    username: str


class AdminUpdateNameResponse(BaseResponse):
    """
    A class that is used to validate the data that is being passed to the `/user/{userId}/update/name` route.

    """

    success: bool
    error: Optional[str]


class CLaimAuthPayload(ORMCamelModel):
    """
    This class is used to claim a user's account
    """

    id: UUID
    email: str


class IGetUserList(CamelModel):
    filter: Optional[GetUser]


class GetAllUsers(GetPages):
    context: Optional[IGetUserList]


class GetUserListItems(PagedResponse):
    items: List[BaseUser]


class GetUserListResponse(PagedBaseResponse):
    response: Optional[GetUserListItems]


class GeneratePassword(BaseModel):
    id: UUID = Field(..., alias='userId')


class NewPassword(CamelModel):
    password: Optional[str]


class GeneratePasswordResponse(BaseResponse):
    response: Optional[NewPassword]