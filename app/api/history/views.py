"""
@author: Kuro
"""
from app import logging
from typing import List, Union, Iterator

from fastapi import APIRouter, Depends, Request
from py_linq import Enumerable
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from app.api.credit.models import Deposit, Withdrawal
from app.api.game.models import PlayerSession, GameList
from app.api.history.models import BetDetailHistory, ActionHistory
from app.api.history.schema import (
    GetBetHistory,
    GetBetHistoryResponse,
    GetActionHistory,
    GetActionHistoryResponse,
    GetCreditHistory,
    GetCreditHistoryResponse, GetWinLoss, TotalWinLossResponse, TotalWinLoss, GetPlayerStatsResponse, StatsData, GetPlayerStatsPage, GetPlayerStatsPages,
    CreditHistory,
)
from app.api.user.models import User
from app.shared.bases.base_model import paginate, Page
from app.shared.middleware.auth import JWTBearer

router = APIRouter(
    prefix="/api/history",
    dependencies=[Depends(JWTBearer())],
    tags=["history"],
)

logger = logging.getLogger("history")
logger.addHandler(logging.StreamHandler())


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


@router.post("/get_credit_history", response_model=GetCreditHistoryResponse)
async def get_credit_history(context: GetCreditHistory, request: Request):
    """
    > This function reads the payment history of a user from the database and returns it

    :param context: GetPaymentHistory - this is the request object that is passed to the function
    :type context: GetCreditHistory
    :param request: Request - this is the request object that is passed to the function.
    :type request: Request
    :return: GetCreditHistoryResponse
    """

    def _get_status(item: Union[Deposit, Withdrawal]) -> bool:
        """
        > This function returns the status of the deposit or withdrawal
        :param item: Union[Deposit, Withdrawal] - this is the item that is being checked
        :return: bool
        """
        return (
            item.status.approval == context.status
            if context.status != 'all'
            else item.status.approval != context.status
        )

    user = User.where(id=context.ownerId).first()
    withdrawals = Enumerable(
        user.userWithdrawals
    )
    deposits = Enumerable(
        user.userDeposits
    )
    transactions = deposits.concat(
        withdrawals
    ).order_by(
        lambda x: x.createdAt
    ).take_while(
        lambda x: _get_status(x)
    )

    def _generate_response() -> Iterator[CreditHistory]:
        """
        > This function generates the response for the credit history
        :return: Iterator[CreditHistory]
        """
        initial_credit = user.creditAccount.balance
        for item in transactions:
            record_type = 'deposit' if isinstance(item, Deposit) else 'withdrawal'
            initial_credit += item.amount if isinstance(item, Deposit) else -item.amount

            yield CreditHistory(
                **dict(
                    transactionId=item.id,
                    amount=item.amount,
                    availableCredit=initial_credit,
                    createdAt=item.createdAt,
                    recordType=record_type,
                    status=item.status.approval,
                    owner=user
                )
            )

    return (
        GetCreditHistoryResponse(success=True, response=list(_generate_response()))
        if user
        else GetCreditHistoryResponse(success=False, error="No history found")
    )


@router.post("/stats/total_win_loss", response_model=TotalWinLossResponse)
async def get_bet_stats(context: GetWinLoss, request: Request):
    """
    > This function returns the win/loss history of a an optional date range

    :param context: GetWinLoss - this is the request object that is passed to the function
    :param request: Request - this is the request object that is passed to the function
    :return: TotalWinLossResponse
    """
    try:
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
    except Exception as e:
        logging.error(e)
        PlayerSession.session.rollback()
        return TotalWinLossResponse(success=False, error="No history found")


@router.post("/stats/game_players", response_model=GetPlayerStatsResponse)
async def get_game_players(context: GetPlayerStatsPage, request: Request):
    """
    > This function returns the win/loss history of a an optional date range

    :param context: GetWinLoss - this is the request object that is passed to the function
    :param request: Request - this is the request object that is passed to the function
    :return: TotalWinLossResponse
    """
    try:
        if total := PlayerSession.session.query(
                PlayerSession.gameSessionId.label("game_session_id"),
                func.count(PlayerSession.id).label("players"),
                func.sum(PlayerSession.betResult).label("winnings"),
        ).group_by(
            PlayerSession.gameSessionId
        ).filter(
            *PlayerSession.filter_expr(
                createdAt__ge=context.context.filter.start_date,
                createdAt__le=context.context.filter.end_date,
                gameSessionId=PlayerSession.gameSessionId
            )
        ):
            game = lambda _total: GameList.where(
                gameSession___id=_total.game_session_id
            ).options(
                joinedload(
                    "gameSession"
                )
            ).first()

            def _build_item_data(items):
                for item in items:
                    yield StatsData(
                        game_session=item.game_session_id,
                        game_id=game(item).id,
                        game_name=game(item).eGameName,
                        players=item.players,
                        winnings=item.winnings,
                    )

            pages = list(_build_item_data(total))
            if bool(context.context.paginate):
                pages = paginate(total, context.params.page, context.params.size)
                pages.items = _build_item_data(pages.items)

            response = GetPlayerStatsPages(

                total_winnings=sum(total.winnings for total in total),
                total_players=sum(total.players for total in total),
                **pages.as_dict() if isinstance(
                    pages, Page
                ) else dict(
                    items=pages if isinstance(pages, list) else pages.items,
                    page=0,
                    pages=0,
                    pageSize=len(pages),
                    total=len(pages)
                )

            )

            return GetPlayerStatsResponse(success=True, response=response)
        return GetPlayerStatsResponse(success=False, error="No history found")
    except Exception as e:
        logging.error(e)
        PlayerSession.session.rollback()
        return GetPlayerStatsResponse(success=False, error="No history found")
