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
from app.shared.schemas.page_schema import GetOptionalContextPages, PagedResponse, Filter, GetPages


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
    userActionHistory:  Optional[User]
    agentActionHistory: Optional[AgentUser]
    adminActionHistory: Optional[Admin]


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


class TotalWinLoss(ORMCamelModel):
    totalWins: Optional[int]
    totalLoss: Optional[int]
    count: Optional[int]


class TotalWinLossResponse(BaseResponse):
    response: Optional[TotalWinLoss]


class GetWinLoss(BaseModel):
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class StatsData(ORMCamelModel):
    game_session: Optional[UUID]
    game_name: Optional[str]
    game_id: Optional[int]
    players: Optional[int]
    winnings: Optional[int]




class GetPlayerStatsData(ORMCamelModel):
    game_data: Optional[List[StatsData]]
    total_winnings: Optional[int]
    total_players: Optional[int]

class StatsPageFilter(BaseModel):
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    game_id: Optional[UUID]
    user_id: Optional[UUID]


class GetPlayerStatsContext(Filter):
    filter: Optional[StatsPageFilter]

class GetPlayerStatsPage(GetOptionalContextPages):
    context: Optional[GetPlayerStatsContext]


class GetPlayerStatsPages(PagedResponse):
    items: Optional[GetPlayerStatsData]


class GetPlayerStatsResponse(BaseResponse):
    response: Optional[GetPlayerStatsPages]


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
