"""
@author: igor
"""
from datetime import datetime
from typing import Optional, Union, List
from uuid import UUID

import pytz
from pydantic import BaseModel, Field

from app.shared.schemas.ResponseSchemas import BaseResponse, PagedBaseResponse
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

    id: Optional[int]
    username: Optional[str]
    phone: Optional[str]


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

