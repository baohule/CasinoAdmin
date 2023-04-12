"""
@author: Kuro
"""
from datetime import datetime
from typing import Optional, Union, List
from uuid import UUID

import pytz
from pydantic import BaseModel

from app.api.agent.schema import AgentUser
from app.api.admin.schema import Admin
from app.shared.schemas.ResponseSchemas import BaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel


class Game(ORMCamelModel):
    """
    `Game` is a class that is used to represent a game
    """

    id: Optional[int]


class User(ORMCamelModel):
    """
    `User` is a class that is used
    to represent a user
    """

    id: Optional[UUID]
    name: Optional[str]
    email: Optional[str]


class BetHistory(ORMCamelModel):
    """
    `BetHistory` is a class that is
    used to represent a bet history
    """

    id: Optional[UUID]
    beforeScore: Optional[int]
    betScore: Optional[int]
    winScore: Optional[int]
    newScore: Optional[int]
    updateAt: Optional[datetime]
    createdAt: Optional[datetime]
    game: Game
    owner: User


class PaymentHistory(ORMCamelModel):
    """
    `PaymentHistory` is a class that is
    used to represent a payment history
    """

    beforeScore: Optional[int]
    changeScore: Optional[int]
    newScore: Optional[int]
    approval: Optional[bool]
    createdAt: Optional[datetime]
    approvedAt: Optional[datetime]
    owner: User


class ActionHistory(ORMCamelModel):
    """
    `ActionHistory` is a class that is used
    to represent an action history
    """

    id: Optional[UUID]
    newValueJson: Optional[str]
    ip: Optional[str]
    createdAt: Optional[datetime]
    owner: Union[User, AgentUser, Admin]


class GetBetHistory(BaseModel):
    """
    `GetBetHistory` is a class that
    is used to represent a request
    """

    ownerId: UUID


class GetActionHistory(BaseModel):
    """
    `GetActionHistory` is a class that
    is used to represent a request
    """

    agentId: Optional[UUID]
    adminId: Optional[UUID]
    userId: Optional[UUID]

    class Config:
        arbitrary_types_allowed = True


class GetPaymentHistory(BaseModel):
    ownerId: UUID


class GetBetHistoryResponse(BaseResponse):
    """
    `GetBetHistoryResponse` is a class that is
    used to represent a response
    """

    response: Optional[List[BetHistory]]


class GetActionHistoryResponse(BaseResponse):
    """
    `GetActionHistoryResponse` is a class that
    is used to represent a response
    """

    response: Optional[List[ActionHistory]]


class GetPaymentHistoryResponse(BaseResponse):
    """
    `GetPaymentHistoryResponse` is a class that
    is used to represent a response
    """

    response: Optional[List[PaymentHistory]]
