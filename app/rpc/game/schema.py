"""
@author: igor
"""
from datetime import datetime
from typing import List, Optional, Any, Dict
from uuid import UUID

from pydantic import BaseModel

from app.shared.schemas.ResponseSchemas import PagedBaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel
from app.api.credit.schema import UserCredit
from app.shared.schemas.page_schema import (
    GetOptionalContextPages,
    PagedResponse,
    Params,
)


class Game(ORMCamelModel):
    id: UUID
    eGameName: Optional[str]
    cGameName: Optional[str]
    type: Optional[int]
    jsonData: Optional[Dict[str, Any]]
    createdAt: Optional[datetime]


class PlayerBet(ORMCamelModel):
    id: Optional[int]
    game_id: Optional[int]
    balance: Optional[UserCredit]
    winscore: Optional[int]
    betscore: Optional[int]
    betline: Optional[int]
    ip: Optional[str]


class PagedGameItems(PagedResponse):
    items: Optional[List[Game]]


class PagedListAllGamesResponse(PagedBaseResponse):
    success: bool
    response: Optional[PagedGameItems]


class ListAllGames(GetOptionalContextPages):
    params: Params