"""
@author: igor
"""
from typing import List, Optional, Any, Dict

from app.shared.schemas.orm_schema import ORMCamelModel

class News(ORMCamelModel):
    username:str
    gameid:int
    gamename:str
    betscore:int
    winscore:int

class NewsList :Optional[List[News]]
