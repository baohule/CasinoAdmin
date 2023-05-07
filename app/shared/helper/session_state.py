from typing import Optional, Dict

from pydantic import BaseModel, Field

from app.api.user.schema import User



class Session(BaseModel):
    sid: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    user: Optional[User] = Field(default=None)


class SocketSession(BaseModel):
    phone_number: Optional[str] = Field(default=None)
    socket_session: Optional[dict] = Field(default=None)
    session: Optional[Session] = Field(default=None)


    def update_session(self, **kwargs):
        if session := self.socket_session.phone_number:
            session.update(**kwargs)
        return self.socket_session

