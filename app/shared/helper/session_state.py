from typing import Optional, Dict

from pydantic import BaseModel, Field

from app.api.user.schema import User
from app.rpc.game.views import GameRoom


class Game(BaseModel):
    game_id: Optional[int] = Field(default=None)
    room: Optional[GameRoom] = Field(default=None)


class Session(BaseModel):
    sid: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    user: Optional[User] = Field(default=None)
    game: Optional[Game] = Field(default=None)


class PhoneNumber(BaseModel):
    __self__: Dict[str, Session] = Field(default={'': {}})


class SocketSession(BaseModel):
    __self__: Optional[PhoneNumber] = Field(default=None)

    def update_session(self: "SocketSession", updated_session: Session) -> "SocketSession":
        for session in self:
            session[1].update(updated_session.dict())
        return self
