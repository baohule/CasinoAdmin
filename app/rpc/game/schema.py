"""
@author: igor
"""
from datetime import datetime
from typing import List, Optional, Any, Dict
from uuid import UUID

import pytz
from pydantic import BaseModel, Field

from app.api.user.schema import User
from app.games.fish.schema import Paths
from app.shared.schemas.ResponseSchemas import PagedBaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel
from app.api.credit.schema import UserCredit
from app.shared.schemas.page_schema import (
    GetOptionalContextPages,
    PagedResponse,
    Params,
)


class Game(ORMCamelModel):
    id: int
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


class GameRoom(BaseModel):
    """
    This class is used to represent a game room.
    """

    game_id: Optional[int]
    room_name: Optional[str]
    players: Optional[List[User]]
    created_at: datetime = Field(default_factory=lambda: datetime.now(pytz.utc))


class RoomList(BaseModel):
    """
    This class is used to represent a list of game rooms.
    """

    rooms: List[GameRoom]


class Game(BaseModel):
    game_id: Optional[int] = Field(default=None)
    room: Optional[GameRoom] = Field(default=None)
    paths: Optional[Paths] = Field(default=None)


class Session(BaseModel):
    sid: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    user: Optional[User] = Field(default=None)
    game: Optional[Game] = Field(default=None)


class PhoneNumber(BaseModel):
    __self__: Dict[str, Session] = Field(default={"": {}})


class SocketSession(BaseModel):
    __self__: Optional[PhoneNumber] = Field(default=None)

    def update_session(
        self: "SocketSession", updated_session: Session
    ) -> "SocketSession":
        for session in self:
            session[1].update(updated_session.dict())
        return self
