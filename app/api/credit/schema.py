"""
@author: Kuro
"""
from typing import Optional, Union
from uuid import UUID

from fastapi_camelcase import CamelModel
from pydantic import Field

from app.shared.schemas.ResponseSchemas import BaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel


class User(ORMCamelModel):
    id: Optional[UUID]
    email: Optional[str]
    name: Optional[str]


class UserCredit(ORMCamelModel):
    """
    `UserCredit` is a class that is used to represent a user credit
    """

    id: Optional[UUID]
    timestamp: Optional[str]
    balance: float = Field(default=0)
    owner: Optional[User]


class GetUserCredit(CamelModel):
    """
    `GetUserCredit` is a class that is used to represent a request
    """

    ownerId: UUID


class GetUserCreditResponse(BaseResponse):
    """
    `GetUserCreditResponse` is a class that is used to represent a response
    """

    response: Optional[UserCredit]


class UpdateUserCredit(CamelModel):
    """
    `UpdateUserCredit` is a class that is used to represent a request
    """

    id: UUID
    balance: float


class UpdateUserCreditResponse(BaseResponse):
    """
    `UpdateUserCreditResponse` is a class that is used to represent a response
    """

    response: Optional[UserCredit]


class DeleteUserCredit(CamelModel):
    """
    `DeleteUserCredit` is a class that is used to represent a request
    """

    id: UUID


class DeleteUserCreditResponse(BaseResponse):
    """
    `DeleteUserCreditResponse` is a class that is used to represent a response
    """

    response: Optional[UUID]


class CreateUserCredit(CamelModel):
    """
    `CreateUserCredit` is a class that is used to represent a request
    """

    balance: float
    ownerId: UUID


class CreateUserCreditResponse(BaseResponse):
    """
    `CreateUserCreditResponse` is a class that is used to represent a response
    """

    response: Optional[UserCredit]
