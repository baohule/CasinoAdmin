"""
@author: Kuro
@github: slapglif
"""
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd
from pydantic import Field, BaseModel, validator
from socketio import AsyncNamespace

from app.api.user.schema import User


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


class ProCount(BaseModel):
    """
    The ProCount class is a class that represents a pro count.
    """

    pro_count: List[List[List[int]]] = Field(default_factory=list)


class BetArr(BaseModel):
    """
    The BetArr class is a class that represents a bet array.
    """

    pro_count: ProCount = Field(default_factory=ProCount)
    hit_times: List[List[int]] = Field(default_factory=list)
    prop_fish_hit_count: List[int] = Field(default_factory=list)


class LoginResponse(BaseModel):
    """
    The LoginResponse class is a class that
    represents a response to a login request.
    """

    tableId: int
    seatId: int


# initialize tableList
table_list = [[None] * 9 for _ in range(3)]
table_list[0][-1] = 0
table_list[1][-1] = 0
table_list[2][-1] = 0


class ClickOdd(BaseModel):
    click: int
    percent: int
    cycle: int
    minpool: int
    maxpool: int


class Player(BaseModel):
    username: str
    table_id: int
    seat_id: int


class Pool(BaseModel):
    pool: int


class FishInfo(BaseModel):
    fish_id: int
    hitInfo: str


class GameInfo(BaseModel):
    totalwin: int
    totalbet: int
    gametype: int


class FishNamespace(AsyncNamespace):
    pool: float = 0
    betCount: List[int] = [1, 5, 10, 20, 30, 50, 100]
    fishList: dict = {}
    virtualPool: float = 0


class GameConfig(BaseModel):
    paths: List[ClickOdd] = [
        ClickOdd(
            **{"click": 10, "percent": 5, "cycle": 2, "minpool": 1, "maxpool": 10}
        ),
        ClickOdd(
            **{"click": 20, "percent": 10, "cycle": 3, "minpool": 2, "maxpool": 20}
        ),
        ClickOdd(
            **{"click": 50, "percent": 20, "cycle": 4, "minpool": 5, "maxpool": 50}
        ),
        ClickOdd(
            **{"click": 100, "percent": 30, "cycle": 5, "minpool": 10, "maxpool": 100}
        ),
        ClickOdd(
            **{"click": 200, "percent": 50, "cycle": 6, "minpool": 15, "maxpool": 200}
        ),
        ClickOdd(
            **{"click": 300, "percent": 80, "cycle": 7, "minpool": 20, "maxpool": 300}
        ),
    ]


class CurrentUser(BaseModel):
    playerclick: int


pro_max = [10, 20, 30]
bet_count = [1, 2, 3]
pro = [0.2, 0.3, 0.4]


class FishNamespace:
    def __init__(self):
        self.del_fish_list = None
        self.fish_list: Dict[str, Dict[int, Fish]] = {}

    def delete_fish(self, table_obj: Dict[int, Fish], fish_id: int) -> None:
        if fish := table_obj.get(fish_id):
            fish.deleted = True
            self.del_fish_list.append(fish)
            del table_obj[fish_id]

    @validator("fish_id")
    def validate_fish_id(cls, v):
        if not isinstance(v, int):
            raise ValueError("fish_id must be an integer")
        elif v < 0:
            raise ValueError("fish_id must be non-negative")
        return v

    # @validator("fish_type")
    # def validate_fish_type(cls, v):
    #     if not isinstance(v, int):
    #         raise ValueError("fish_type must be an integer")
    #     elif v < 0 or v >= len():
    #         raise ValueError(f"fish_type {v} out of range")
    #     return v
    #


class HitTimes:
    pass


class PoolInfo(BaseModel):
    pool: int
    virtualPool: int


class SkillInfo(BaseModel):
    sid: int


class Boom:
    pass


def RandomNumBoth(Min: int, Max: int) -> int:
    """
    The function generates a random integer between a minimum and maximum value.

    :param Min: The minimum value of the range from which a random number will be generated
    :type Min: int
    :param Max: The maximum value that the random number can take
    :type Max: int
    :return: The function `RandomNumBoth` returns a random integer between the minimum value `Min` and the maximum value `Max`.
    """
    Range = Max - Min
    Rand = pd.core.dtypes.common.random.rand()
    return Min + round(Rand * Range)


class Fish(BaseModel):
    """
    The Fish class is a Pydantic model that represents a
    fish in the game. It contains the following attributes:
    """

    fish_id: int
    fish_type: int
    fish_path: str
    coin: int
    fish_count: int


class FishOut(BaseModel):
    """
    The FishOut class is a Pydantic model that represents
    a fish out event in the game. It contains the following attributes:
    """

    fishOutList: List[int] = []
    fishOutProMax: int = 0

    class LoginParams(User):
        userlist: Optional[dict]

    class LoginResponse(BaseModel):
        tableId: int
        seatId: int

    class Room(BaseModel):
        roomid: Optional[str]
        onlienPepole: int = 0
        tableMax: int = 10
        seatMax: int = 4
        tableList: List[str]  #  = Field(default_factory=lambda: [[None] * 5] * 10)


class Objective(BaseModel):
    """
    The Objective class is a Pydantic model that represents
    a game objective. It contains the following attributes:
    """

    id: int
    reward: int
    hit_times: int
    type: int


class Path(BaseModel):
    """
    The Path class is a Pydantic model that represents
    a game path. It contains the following attributes:
    - duration = Column(DateTime)
    - starting = Column(Float)
    - middle = Column(Float)
    - destination = Column(Float)
    """

    id: int
    duraton: datetime
    starting: float
    middle: float
    destination: float
    taken: bool = False


class Paths(BaseModel):
    """
    The Paths class is a Pydantic model that represents
    a game path. It contains the following attributes:
    """

    __self__: List[Path] = []
