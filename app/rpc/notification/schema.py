"""
@author: igor
"""
from typing import List, Optional, Any, Dict

from app.shared.schemas.orm_schema import ORMCamelModel


class News(ORMCamelModel):
    username: str
    game_id: int
    game_name: str
    bet_score: int
    win_score: int


class NewsList:
    items: Optional[List[News]]
