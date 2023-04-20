"""
@author: Kuro
"""
from typing import Tuple

from pydantic import BaseModel
from sqlalchemy import func, and_, subquery, select, case, Column
from sqlalchemy.orm import aliased, load_only
from sqlalchemy.sql import Select, Alias
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.operators import is_

from app.api.game.models import PlayerSession, GameSession, GameList
from app.api.history.models import PaymentHistory, BetDetailHistory, ActionHistory
from fastapi import APIRouter, Depends, Request

from app.api.history.schema import (
    GetBetHistory,
    GetBetHistoryResponse,
    GetActionHistory,
    GetActionHistoryResponse,
    GetPaymentHistory,
    GetPaymentHistoryResponse, GetWinLoss, TotalWinLossResponse, TotalWinLoss, GetPlayerStatsResponse, GetPlayerStats, StatsData, Game,
)
from app.api.user.models import User
from app.shared.middleware.auth import JWTBearer
from fastapi.exceptions import HTTPException
import logging

router = APIRouter(
    prefix="/api/history",
    dependencies=[Depends(JWTBearer())],
    tags=["history"],
)


@router.post("/get_bet_history", response_model=GetBetHistoryResponse)
async def get_bet_history_(context: GetBetHistory, request: Request):
    """
    `   "Get the bet history for the given bet id."

        :param context: GetBetHistory - this is the request object that is passed in from the client
        :type context: GetBetHistory
        :param request: Request - this is the request object that is passed to the function
        :type request: Request
        :return: GetBetHistoryResponse
    """
    history = BetDetailHistory.read_all(**context.dict())
    return (
        GetBetHistoryResponse(success=True, response=history)
        if history
        else GetBetHistoryResponse(success=False, error="No history found")
    )


@router.post("/get_action_history", response_model=GetActionHistoryResponse)
async def get_action_history_(context: GetActionHistory, request: Request):
    """
    "Get the action history for the given action id."

    :param context: GetActionHistory - this is the request object that will be sent to the function
    :type context: GetActionHistory
    :param request: Request - This is the request object that is passed to the function
    :type request: Request
    :return: GetActionHistoryResponse
    """
    history = ActionHistory.read_all(**context.dict(exclude_unset=True, exclude_none=True))
    return (
        GetActionHistoryResponse(success=True, response=history)
        if history
        else GetActionHistoryResponse(success=False, error="No history found")
    )


@router.post("/get_payment_history", response_model=GetPaymentHistoryResponse)
async def get_payment_history_(context: GetPaymentHistory, request: Request):
    """
    > This function reads the payment history of a user from the database and returns it

    :param context: GetPaymentHistory - this is the request object that is passed to the function
    :type context: GetPaymentHistory
    :param request: Request - this is the request object that is passed to the function.
    :type request: Request
    :return: GetPaymentHistoryResponse
    """
    history = PaymentHistory.read_all(**context.dict())
    return (
        GetPaymentHistoryResponse(success=True, response=history)
        if history
        else GetPaymentHistoryResponse(success=False, error="No history found")
    )


@router.post("/stats/total_win_loss", response_model=TotalWinLossResponse)
async def get_bet_stats(context: GetWinLoss, request: Request):
    """
    > This function returns the win/loss history of a an optional date range

    :param context: GetWinLoss - this is the request object that is passed to the function
    :param request: Request - this is the request object that is passed to the function
    :return: TotalWinLossResponse
    """
    if total := PlayerSession.session.query(
            select([
                func.sum(PlayerSession.betResult).label("wins"),
                func.count(PlayerSession.betResult).label("win_count")
            ]).filter(
                *PlayerSession.filter_expr(
                    betResult__lt=0
                )).subquery(),
            select([
                func.sum(PlayerSession.betResult).label("losses"),
                func.count(PlayerSession.betResult).label("loss_count")
            ]).filter(
                *PlayerSession.filter_expr(
                    betResult__gt=0
                )).subquery()
    ).filter(
        *PlayerSession.filter_expr(
            createdAt__ge=context.start_date,
            createdAt__le=context.end_date,
        )
    ).first():
        logging.debug(total)
        total_count = total.loss_count + total.win_count
        response = TotalWinLoss(totalLoss=total.losses, totalWins=total.wins, count=total_count)
        return TotalWinLossResponse(success=True, response=response)
    return TotalWinLossResponse(success=False, error="No history found")


@router.post("/stats/game_players", response_model=GetPlayerStatsResponse)
async def get_game_players(context: GetPlayerStats, request: Request):
    """
    > This function returns the win/loss history of a an optional date range

    :param context: GetWinLoss - this is the request object that is passed to the function
    :param request: Request - this is the request object that is passed to the function
    :return: TotalWinLossResponse
    """
    if total := PlayerSession.session.query(
            PlayerSession.gameSessionId.label("game_session_id"),
            func.count(PlayerSession.id).label("players"),
            func.sum(PlayerSession.betResult).label("winnings"),
    ).group_by(
        PlayerSession.gameSessionId
    ).filter(
        *PlayerSession.filter_expr(
            createdAt__ge=context.start_date,
            createdAt__le=context.end_date,
            gameSessionId=PlayerSession.gameSessionId
        )
    ):
        game = lambda _total: GameList.where(gameSession___id=_total.game_session_id).options(joinedload("gameSession")).first()
        print(game)
        response = [
            StatsData(
                game_session=total.game_session_id,
                game_id=game(total).id,
                game_name=game(total).eGameName,
                players=total.players,
                winnings=total.winnings
            )
            for total in total
        ]
        return GetPlayerStatsResponse(success=True, response=response)
    return GetPlayerStatsResponse(success=False, error="No history found")
