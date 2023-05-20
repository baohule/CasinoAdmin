"""
@author: igor
"""
from datetime import date, datetime
from typing import Optional, List, Union
from uuid import UUID
import re

from app.shared.schemas.orm_schema import Schema
from pydantic import EmailStr, validator, Field

from app.api.auth.schema import TokenDetail, TokenResponse
from app.shared.schemas.RequestSchemas import GetAwaitable
from app.shared.schemas.ResponseSchemas import BaseResponse, PagedBaseResponse
from app.shared.schemas.orm_schema import ORMSchema

from typing import Optional
from pydantic import BaseModel

from app.shared.schemas.page_schema import GetPages, PagedResponse


class UserLogin(GetAwaitable):
    phone_number: Optional[str]


class UserCredit(ORMSchema):
    balance: Optional[float]
    updatedAt: Optional[datetime]


class User(ORMSchema):
    id: Optional[int]
    phone: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    phoneNumber: Optional[str]
    balance: Optional[UserCredit]
    username: Optional[str]
    createdAt: Optional[datetime]
    active: Optional[bool]
    accessToken: Optional[str]


class UserResponse(BaseResponse):
    """
    `UserResponse` is a class that is used to validate a user response
    """

    response: Optional[User]


class BaseUser(ORMSchema):
    """
    `User` is a class that is used to validate the data that is being passed to the `/user` route.
    """

    id: Optional[int]
    phone: Optional[str]
    username: Optional[str]
    phoneNumber: Optional[str]
    headImage: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    creditAccount: Optional[UserCredit]
    active: Optional[bool]


class Game(ORMSchema):
    id: Optional[int]
    name: Optional[str]
    users: Optional[List[User]]


class Room(ORMSchema):
    id: Optional[UUID]
    name: Optional[str]
    game: Optional[Game]
    users: Optional[List[User]]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


class Socket(ORMSchema):
    id: Optional[str]
    rooms: Optional[List[Room]]
    user: Optional[User]


class UserSession(ORMSchema):
    id: Optional[int]
    game: Optional[Game] = Field(default=None)
    room: Optional[Room] = Field(default=None)
    user: Optional[User]
