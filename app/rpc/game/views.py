"""
@author: igor
"""

from fastapi import Request

from app.api.game.models import GameList
from app.rpc.game.schema import PlayerBet
from app.rpc.game.schema import (
    PagedListAllGamesResponse,
    ListAllGames,
)

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

def insert_player_bet_history(content:PlayerBet):
    """
    """
