"""
@author: igor
"""
import time
from datetime import datetime
from typing import List, Optional

import pytz
from py_linq import Enumerable
from pydantic import BaseModel, Field
from realtime import timestamp

from app import main_socket

from fastapi import Request

from app.api.game.models import GameList
from app.api.user.models import User
from app.rpc.user.schema import BaseUser
from app.rpc.auth.views import default_session
from app.rpc.game.schema import PlayerBet
from app.rpc.game.schema import (
    PagedListAllGamesResponse,
    ListAllGames,
)
from app.shared.helper.session_state import SocketSession, Session
from app.shared.schemas.ResponseSchemas import BaseResponse
from app import redis


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


def insert_player_bet_history(content: PlayerBet):
    """
    """


class GameRoom(BaseModel):
    """
    This class is used to represent a game room.
    """

    game_id: Optional[int]
    room_name: Optional[str]
    players: Optional[List[BaseUser]]
    created_at: datetime = Field(default_factory=lambda: datetime.now(pytz.utc))


class RoomList(BaseModel):
    """
    This class is used to represent a list of game rooms.
    """

    rooms: List[GameRoom]


async def get_active_rooms(session: Session, context: PlayerBet):
    """
    This function is used to create a new game room.
    :param session:
    :param context:
    :return:
    """
    game = GameList.read(id=context.game_id)
    user = User.read(id=session.user.id)
    active_rooms = RoomList(
        rooms=[
            GameRoom(**room) for room in await redis.get('rooms')
        ]
    )

    if not active_rooms:
        room_name = f"{context.game_id}-{int(time.time())}"
        active_rooms = RoomList(
            rooms=[
                GameRoom(
                    game_id=context.game_id,
                    room_name=room_name,
                    players=[user],
                    created_at=datetime.now()
                )
            ]
        )
    if (
            game_room := Enumerable(active_rooms.rooms)
                    .where(
                lambda room: room.game_id == context.game_id
                             and len(room.players) < game.max_players
                             and Enumerable(room.players)
                                     .where(lambda player: player.id != user.id)
                                     .first()
            ).first()
    ):
        pass


    #     if (
    #             Enumerable(active_rooms.rooms)
    #                     .where(lambda room: room.name == game_room.name)
    #                     .first()
    #     ):
    #         return BaseResponse(success=False, error="Room is already active")
    #
    #     active_rooms.rooms.append(game_room)
    #
    #     game_room.players.append(user)
    #     updated_session = session.dict()
    #     updated_session.get(user.phoneNumber).update(
    #         {
    #             "game": {
    #                 "game_id": context.game_id,
    #                 "room": game_room.json()
    #             }
    #         }
    #     )
    #     await main_socket.save_session(session.sid, updated_session)
    #
    # await redis.set('rooms', active_rooms.json())
    # return active_rooms


@main_socket.on("loginRoom")
async def login_room(socket_id, context: PlayerBet):
    """
    This function is used to login to a game room.

    :param socket_id: The `socket_id` parameter is the id of the socket
    :type socket_id: str
    :param context: The `context` parameter is of type PlayerBet
    :type context: PlayerBet
    :return: None
    """

    socket_session = main_socket.get_session(socket_id)
    if not socket_session:
        return BaseResponse(success=False, error="Session not found, log in again")
    session_data = Enumerable(socket_session.dict().values()).first()
    session = Session(**session_data)
    active_room = get_active_rooms(session, context)
    if not active_room:
        return BaseResponse(success=False, error="No room available")
    await main_socket.enter_room(socket_id, session.game.game_id, namespace=session.game.room.room_name)
    redis.set(f"{context.game_id}-{int(time.time())}", socket_id)
    await main_socket.emit("loginRoom", data=context.dict(), room=context.game_id)


@main_socket.on("logoutRoom")
async def logout_room(socket_id, context: PlayerBet):
    """
    This function logs out a player from a game room and emits a "logoutRoom" event to all players in the room.

    :param socket_id: The ID of the socket connection that is being used to communicate with the server
    :param context: The `context` parameter is an instance of the `PlayerBet` class, which contains information about the player's bet in the game. It is used to identify the game the
    player is currently in, so that the player can be logged out of that game's room
    :type context: PlayerBet
    """
    game = GameList.read(id=context.game_id)

    socket_session = main_socket.get_session(socket_id)
    if not socket_session:
        return BaseResponse(success=False, error="Session not found, log in again")
    session_data = Enumerable(socket_session.dict().values()).first()
    session = Session(**session_data)
    if not session.game:
        return BaseResponse(success=False, error="No game found")
    if not session.game.room:
        return BaseResponse(success=False, error="No players found")

    if not Enumerable(
            session.game.room.players.where(
                lambda player: player.id == session.user.id
            ).first()
    ):
        pass

    #     return BaseResponse(success=False, error="Player not found")
    # if not Enumerable(
    #         session.game.room.players.where(
    #             lambda player: player.id != session.user.id
    #         ).first()
    #                 .bets
    #                 .where(
    #             lambda bet: bet.player_id == session.user.id
    #                         and bet.game_id == context.game_id
    #                         and bet.status == "pending"
    #                         and bet.amount == context.amount
    #                         and bet.type == context.type
    #                         and bet.round == context.round
    #                         and bet.timestamp == context.timestamp
    #                         and bet.player_id == context.player_id
    #                         and bet.player_name == context.player_name
    #                         and bet.player_hand == context.player_hand
    #                         and bet.player_hand_value == context.player_hand_value
    #                         and bet.dealer_hand == context.dealer_hand


    #
    # await main_socket.leave_room(socket_id, context.game_id, namespace=game.eGameName)
    # await main_socket.emit("logoutRoom", data=context.dict(), room=context.game_id)
