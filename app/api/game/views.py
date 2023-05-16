"""
@author: Kuro
"""
from app import logging

from fastapi import APIRouter, Depends, Request

from app.api.game.models import GameList
from app.api.game.schema import (
    CreateGame,
    GetGame,
    UpdateGame,
    CreateGameResponse,
    GetGameResponse,
    UpdateGameResponse,
    PagedListAllGamesResponse,
    ListAllGames,
    PagedGameItems,
)
from app.shared.middleware.auth import JWTBearer

router = APIRouter(
    prefix="/api/game",
    dependencies=[Depends(JWTBearer())],
    tags=["game"],
)

logger = logging.getLogger("game")
logger.addHandler(logging.StreamHandler())


@router.post("/manage/create_game", response_model=CreateGameResponse)
async def create_game(context: CreateGame, request: Request) -> CreateGameResponse:
    """
    > Create a new game in the database

    :param context: CreateGame - This is the request object that we created in the previous step
    :type context: CreateGame
    :param request: Request - This is the request object that is passed to the function
    :type request: Request
    :return: CreateGameResponse
    """
    _game = context.dict()
    new_game = GameList.create(**_game)
    return (
        CreateGameResponse(success=True, response=new_game)
        if new_game
        else CreateGameResponse(success=False, error="Object exists")
    )


@router.post("/manage/get_game", response_model=GetGameResponse)
async def get_game(context: GetGame, request: Request) -> GetGameResponse:
    """
    > This function returns a list of games owned by the user with the given id

    :param context: GetGame - this is the context object that is passed to the function.
    :type context: GetGame
    :param request: Request - This is the request object that is passed to the function
    :type request: Request
    :return: A list of games
    """

    objects = GameList.read(ownerId=context.id)
    return GetGameResponse(success=True, response=objects)


@router.post("/manage/update_game", response_model=UpdateGameResponse)
async def update_game(context: UpdateGame, request: Request) -> UpdateGameResponse:
    """
    > Update the game balance for a given game id

    :param context: UpdateGame - This is the context of the request.
    :type context: UpdateGame
    :param request: The incoming request
    :type request: Request
    :return: The updated game is being returned.
    """
    _game = context.dict()
    updated_game = GameList.update(id=_game.get("id"), balance=_game.get("balance"))
    return UpdateGameResponse(success=True, response=updated_game)


@router.post("/manage/get_all_games", response_model=PagedListAllGamesResponse)
def get_all_games(context: ListAllGames, request: Request):
    """
    This function retrieves a list of all games with pagination.

    :param context: The context parameter is of type ListAllGames
    :type context: ListAllGames
    :param request: The `request` parameter is an instance of the `Request` class
    :type request: Request
    :return: a PagedListAllGamesResponse object with a success flag set to True and a
    response attribute containing a list of games.
    """
    games = GameList.list_all_games(
        page=context.params.page, num_items=context.params.size
    )
    return PagedListAllGamesResponse(success=True, response=games)
