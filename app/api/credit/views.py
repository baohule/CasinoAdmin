"""
@author: Kuro
"""
from fastapi import APIRouter, Depends, Request

from app.api.agent.models import Agent
from app.api.credit import schema
from app.api.credit.models import Balance, Deposit, Status, Withdrawal
from app.api.credit.schema import (
    CreateUserCreditResponse,
    CreateUserCredit,
    UserCredit,
    GetUserCredit,
    GetUserCreditResponse,
    UpdateUserCreditResponse,
    UpdateUserCredit, UpdateAgentQuotaResponse, UpdateAgentQuota, GetUserWithdrawals, GetUserWithdrawalsResponse, GetUserDepositsResponse, GetUserDeposits,
)
from app.shared.middleware.auth import JWTBearer
from app.shared.schemas.ResponseSchemas import BaseResponse

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


@router.post("/manage/update_user_credit", response_model=UpdateUserCreditResponse)
async def update_credit(context: UpdateUserCredit, request: Request):
    """
    `update_credit` updates the credit of a user

    :param context: schema.UpdateUserCredit
    :type context: schema.UpdateUserCredit
    :param request: Request - The request object that was sent to the server
    :type request: Request
    :return: The updated credit object.
    """
    balance = Balance.read(ownerId=context.ownerId)
    agent = Agent.read(id=request.user.id)
    if not agent:
        return BaseResponse(success=False, error="Agent not found")
    if agent.agent_quota < context.balance:
        return BaseResponse(success=False, error="Agent Quota Exceeded")
    if not balance:
        return BaseResponse(success=False, error="User Has no Credit Account")
    _updated = Balance.update(**context.dict())
    _agent_updated = Agent.update(
        id=agent.id, agent_quota=agent.agent_quota - context.balance
    )

    return UpdateUserCreditResponse(success=True, response=UserCredit(**context.dict()))


@router.post("/manage/update_agent_quota", response_model=UpdateAgentQuotaResponse)
async def update_agent_quota(context: UpdateAgentQuota, request: Request):
    """
    `update_agent_quota` updates the quota of an agent
    :param context: UpdateAgentQuota
    :param request: Request
    :return:  UpdateAgentQuotaResponse
    """
    agent = Agent.read(id=request.user.id)
    if not agent:
        return BaseResponse(success=False, error="Agent not found")
    _updated = Agent.update(**context.dict())
    return (
        UpdateAgentQuotaResponse(
            success=True, response=Agent(**context.dict())
        )
        if _updated
        else BaseResponse(success=False, error="Could not update agent quota")
    )


@router.post("/manage/deposit", response_model=UpdateUserCreditResponse)
async def deposit(context: UpdateUserCredit, request: Request):
    """
    `deposit` deposits money into a user's account
    :param context: contains the ownerId and the amount to deposit
    :param request: Request object
    :return: UpdateUserCreditResponse
    """
    if (
            _ := Deposit.read_all(ownerId=context.ownerId)
                    .join(Status, isouter=True)
                    .filter(Status.status == "Pending")
                    .first()
    ):
        return BaseResponse(success=False, error="User has pending deposit")
    _deposit = Deposit.create(**context.dict())
    return UpdateUserCreditResponse(success=True, response=_deposit)


@router.post("/manage/approve_deposit", response_model=UpdateUserCreditResponse)
async def approve_deposit(context: UpdateUserCredit, request: Request):
    """
    `approve_deposit` approves a deposit request
    :param context: contains the ownerId and the amount to deposit
    :param request: Request object
    :return: UpdateUserCreditResponse
    """
    _deposit = Deposit.read(ownerId=context.ownerId)
    if not _deposit:
        return BaseResponse(success=False, error="Deposit not found")
    _Status = Status.create(
        depositId=_deposit.id, status="approved", approvedBy=request.user.id
    )
    if not _Status:
        return BaseResponse(success=False, error="Could not approve deposit")
    _updated = Balance.update(
        ownerId=context.ownerId, balance=_deposit.balance + context.balance
    )
    return UpdateUserCreditResponse(success=True, response=_updated)


@router.post("/manage/reject_deposit", response_model=UpdateUserCreditResponse)
async def reject_deposit(context: UpdateUserCredit, request: Request):
    """
    `reject_deposit` rejects a deposit request
    :param context: contains the ownerId and the amount to deposit
    :param request: Request object
    :return: UpdateUserCreditResponse
    """
    _deposit = Deposit.read(ownerId=context.ownerId)
    if not _deposit:
        return BaseResponse(success=False, error="Deposit not found")
    _Status = Status.create(
        depositId=_deposit.id, status="rejected", approvedBy=request.user.id
    )
    return (
        UpdateUserCreditResponse(success=True, response=_deposit)
        if _Status
        else BaseResponse(success=False, error="Could not reject deposit")
    )


@router.post("/manage/withdraw", response_model=UpdateUserCreditResponse)
async def withdraw(context: UpdateUserCredit, request: Request):
    """
    `withdraw` withdraws money from a user's account
    :param context: contains the ownerId and the amount to withdraw
    :param request: Request object
    :return: UpdateUserCreditResponse
    """
    if (
            _ := Withdrawal.where(ownerId=context.ownerId)
                    .join(Status, isouter=True)
                    .filter(Status.status == "Pending")
                    .first()
    ):
        return BaseResponse(success=False, error="User has pending withdrawal")
    _withdraw = Withdrawal.create(**context.dict())
    return UpdateUserCreditResponse(success=True, response=_withdraw)


@router.post("/manage/approve_withdraw", response_model=UpdateUserCreditResponse)
async def approve_withdraw(context: UpdateUserCredit, request: Request):
    """
    `approve_withdraw` approves a withdrawal request
    :param context: contains the ownerId and the amount to withdraw
    :param request: Request object
    :return: UpdateUserCreditResponse
    """
    _withdraw = Withdrawal.read(ownerId=context.ownerId)
    if not _withdraw:
        return BaseResponse(success=False, error="Withdrawal not found")
    _Status = Status.create(
       status="approved", approvedById=request.user.id
    )
    if not _Status:
        return BaseResponse(success=False, error="Could not approve withdrawal")
    _updated = Balance.update(
        ownerId=context.ownerId, balance=Balance.balance - Withdrawal.amount
    )
    return UpdateUserCreditResponse(success=True, response=_updated)


@router.post("/manage/reject_withdraw", response_model=UpdateUserCreditResponse)
async def reject_withdraw(context: UpdateUserCredit, request: Request):

    _withdraw = Withdrawal.read(ownerId=context.ownerId)
    if not _withdraw:
        return BaseResponse(success=False, error="Withdrawal not found")
    _Status = Status.create(
        withdrawId=Withdrawal.id, status="rejected", approvedBy=request.user.id
    )
    return (
        UpdateUserCreditResponse(success=True, response=_withdraw)
        if _Status
        else BaseResponse(success=False, error="Could not reject withdrawal")
    )


@router.post("/manage/get_user_withdrawals", response_model=GetUserWithdrawalsResponse)
async def get_user_withdrawals(context: GetUserWithdrawals, request: Request):
    """
    `get_user_withdrawals` gets all the withdrawals for a user
    :param context: GetUserWithdrawals
    :param request: Request
    :return: GetUserWithdrawalsResponse
    """
    withdrawals = Withdrawal.read_all(**context.dict(exclude_unset=True))
    return GetUserWithdrawalsResponse(
        success=True, response=withdrawals
    )


@router.post("/manage/get_user_deposits", response_model=GetUserDepositsResponse)
async def get_user_deposits(context: GetUserDeposits, request: Request):
    """
    `get_user_deposits` gets all the deposits for a user
    :param context: GetUserDeposits
    :param request: Request
    :return: GetUserDepositsResponse
    """
    deposits = Deposit.read_all(**context.dict(exclude_unset=True))
    return GetUserDepositsResponse(
        success=True, response=deposits
    )