"""
@author: Kuro
@github: slapglif
"""



from typing import Dict

from pydantic import Field, BaseModel


class LoginRoomResult(BaseModel):
    success: bool = Field(True)
    session_id: str = Field(...)

class PlayerOut(BaseModel):
    user_id: int = Field(...)
    session_id: str = Field(...)

class HitResult(BaseModel):
    success: bool = Field(...)
    updated_fish: Dict[str, int] = Field(...)

class UserScore(BaseModel):
    user_id: int = Field(...)
    score: int = Field(...)
