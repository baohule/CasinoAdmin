from typing import List, Optional, Any, Dict
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.shared.schemas.ResponseSchemas import BaseResponse, PagedBaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel
from app.shared.schemas.page_schema import GetOptionalContextPages, PagedResponse, GetPages, Filter, Params


class Game(ORMCamelModel):
    id: UUID
    eGameName: Optional[str]
    cGameName: Optional[str]
    type: Optional[int]
    jsonData: Optional[Dict[str, Any]]
    createdAt: Optional[datetime]


class PagedGameItems(PagedResponse):
    items: Optional[List[Game]]


class PagedListAllGamesResponse(PagedBaseResponse):
    success: bool
    response: Optional[PagedGameItems]



class ListAllGames(GetOptionalContextPages):
    params: Params



class UpdateGameResponse(BaseModel):
    success: bool
    response: Optional[Game]


class CreateGameResponse(BaseModel):
    success: bool
    response: Optional[Game]
    error: Optional[str]


class GetGameResponse(BaseModel):
    success: bool
    response: Optional[Game]
    error: Optional[str]


class CreateGame(BaseModel):
    username: str
    description: str

class UpdateGame(BaseModel):
    id: UUID
    username: str
    description: str

class RemoveGame(BaseModel):
    id: UUID

class GetGame(BaseModel):
    id: UUID



