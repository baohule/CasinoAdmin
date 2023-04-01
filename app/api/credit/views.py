"""
@author: Kuro
"""
from fastapi import APIRouter, Depends, Request
from app.api.credit import schema
from app.api.credit.models import Balance
from app.api.credit.schema import (
    CreateUserCreditResponse,
    CreateUserCredit,
    UserCredit,
    GetUserCredit,
    GetUserCreditResponse,
    UpdateUserCreditResponse,
    UpdateUserCredit,
)
from app.shared.middleware.auth import JWTBearer


router = APIRouter(
    prefix="/api/credit",
    dependencies=[Depends(JWTBearer())],
    tags=["credit"],
)


@router.post("/manage/create_user_credit", response_model=CreateUserCreditResponse)
async def create_credit(context: CreateUserCredit, request: Request):
    """
    `create_credit` creates a new credit object for a user
    :param context:
    :param request:
    :return: BaseResponse
    """
    _create_credit: UserCredit = Balance.create(
        ownerId=context.ownerId, balance=context.balance
    )
    return (
        CreateUserCreditResponse(success=True, response=_create_credit)
        if _create_credit
        else CreateUserCreditResponse(success=False, error="Object exists")
    )


@router.post("/manage/get_user_credit", response_model=schema.GetUserCreditResponse)
async def get_credit(context: GetUserCredit, request: Request):
    """
    It returns the credit of the user with the given ID

    :param context: schema.GetUserCredit
    :type context: schema.GetUserCredit
    :param request: The request object that was sent to the server
    :type request: Request
    :return: A credit object
    """
    user_credits = Balance.read(ownerId=context.ownerId)
    return GetUserCreditResponse(success=True, response=user_credits)


@router.post(
    "/manage/update_user_credit", response_model=schema.UpdateUserCreditResponse
)
async def update_credit(context: UpdateUserCredit, request: Request):
    """
    `update_credit` updates the credit of a user

    :param context: schema.UpdateUserCredit
    :type context: schema.UpdateUserCredit
    :param request: Request - The request object that was sent to the server
    :type request: Request
    :return: The updated credit object.
    """
    _updated = Balance.update(id=context.id, balance=context.balance)
    return UpdateUserCreditResponse(success=True, response=UserCredit(**context.dict()))
