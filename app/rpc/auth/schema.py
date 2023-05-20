"""
@author: igor
"""
import json
from typing import Optional, Dict, List

from app.shared.schemas.orm_schema import Schema
from pydantic import Field, EmailStr, BaseModel, validator
from uuid import UUID

from app.rpc.user.schema import UserSession
from app.shared.helper.session_state import SocketSession


class OTPInput(BaseModel):
    phone_number: str = Field(example="19299338861")
    code: Optional[int]


class AccesToken(BaseModel):
    access_token: str


class RedisUser(BaseModel):
    __self__: Dict[str, UserSession]


class RedisUsers(BaseModel):
    @validator("users")
    def validate_message(cls, v):
        for item in v:
            if isinstance(v, dict):
                yield json.dumps(item)

    users: Optional[List[Optional[SocketSession]]]
