"""
@author: Kuro
"""
from app.api.history.models import PaymentHistory, BetDetailHistory, ActionHistory
from fastapi import APIRouter, Depends, Request

from app.api.history.schema import (
    GetBetHistory,
    GetBetHistoryResponse,
    GetActionHistory,
    GetActionHistoryResponse,
    GetPaymentHistory,
    GetPaymentHistoryResponse,
)
from app.shared.middleware.auth import JWTBearer
from fastapi.exceptions import HTTPException

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
