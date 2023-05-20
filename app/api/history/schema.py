"""
@author: Kuro
"""
from datetime import datetime
from typing import Optional, Union, List
from uuid import UUID

import pytz
from pydantic import BaseModel, Field

from app.api.agent.schema import AgentUser
from app.api.admin.schema import Admin
from app.shared.schemas.ResponseSchemas import BaseResponse, PagedBaseResponse
from app.shared.schemas.orm_schema import ORMSchema
from app.shared.schemas.page_schema import (
    GetOptionalContextPages,
    PagedResponse,
    Filter,
    GetPages,
)


class Game(ORMSchema):
    """
    `Game` is a class that is used to represent a game
    """

    id: Optional[int]


class User(ORMSchema):
    """
    `User` is a class that is used
    to represent a user
    """

    id: Optional[int]
    username: Optional[str]
    phone: Optional[str]


class BetHistory(ORMSchema):
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


class CreditHistory(ORMSchema):
    """
    `PaymentHistory` is a class that is
    used to represent a payment history
    """

    transactionId: Optional[UUID]
    amount: Optional[int]
    availableCredit: Optional[int]
    createdAt: Optional[datetime]
    recordType: Optional[str]
    status: Optional[str]
    owner: Optional[User]


class ActionHistory(ORMSchema):
    """
    `ActionHistory` is a class that is used
    to represent an action history
    """

    id: Optional[UUID]
    newValueJson: Optional[str]
    ip: Optional[str]
    createdAt: Optional[datetime]
    userActionHistory: Optional[User]
    agentActionHistory: Optional[AgentUser]
    adminActionHistory: Optional[Admin]


class GetBetHistory(BaseModel):
    """
    `GetBetHistory` is a class that
    is used to represent a request
    """

    ownerId: int


class GetActionHistory(BaseModel):
    """
    `GetActionHistory` is a class that
    is used to represent a request
    """

    agentId: Optional[UUID]
    adminId: Optional[UUID]
    userId: Optional[int]

    class Config:
        arbitrary_types_allowed = True


class GetCreditHistory(BaseModel):
    ownerId: int
    status: Optional[str] = Field(default="all")


class TotalWinLoss(ORMSchema):
    totalWins: Optional[int]
    totalLoss: Optional[int]
    count: Optional[int]


class TotalWinLossResponse(BaseResponse):
    response: Optional[TotalWinLoss]


class GetWinLoss(BaseModel):
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class StatsData(ORMSchema):
    game_session: Optional[UUID]
    game_name: Optional[str]
    game_id: Optional[int]
    players: Optional[int]
    winnings: Optional[int]


class GetPlayerStatsData(ORMSchema):
    items: Optional[List[StatsData]]
    total_winnings: Optional[int]
    total_players: Optional[int]


class StatsPageFilter(BaseModel):
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    game_id: Optional[int]
    user_id: Optional[int]


class GetPlayerStatsContext(Filter):
    filter: Optional[StatsPageFilter]
    paginate: Optional[bool] = Field(default=True)


class GetPlayerStatsPage(GetOptionalContextPages):
    context: Optional[GetPlayerStatsContext]


class GetPlayerStatsPages(PagedResponse):
    items: Optional[List[StatsData]]
    total_winnings: Optional[int]
    total_players: Optional[int]


class GetPlayerStatsResponse(PagedBaseResponse):
    response: Optional[
        Union[Optional[GetPlayerStatsPages], Optional[GetPlayerStatsData]]
    ]


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


class GetCreditHistoryResponse(BaseResponse):
    """
    `GetCreditHistoryResponse` is a class that
    is used to represent a response
    """

    response: Optional[List[CreditHistory]]
