"""
@author: Kuro
"""
from app import logging

from fastapi import APIRouter, Depends, Request

from app.api.admin.models import Admin
from app.api.agent.models import Agent
from app.api.credit import schema
from app.api.credit.models import Balance, Deposit, Status, Withdrawal, Quota
from app.api.credit.schema import (
    CreateUserCreditResponse,
    CreateUserCredit,
    UserCredit,
    GetUserCredit,
    GetUserCreditResponse,
    UpdateUserCreditResponse,
    UpdateUserCredit,
    UpdateAgentQuotaResponse,
    UpdateAgentQuota,
    GetUserWithdrawals,
    GetUserWithdrawalsResponse,
    GetUserDepositsResponse,
    GetUserDeposits,
    DepositResponse,
    WithdrawalResponse,
    GetWithdrawal,
    GetDeposit,
    ChangeDepositStatusResponse,
    ChangeWithdrawalStatusResponse,
    MakeWithdrawal,
    BalanceDeposit,
    BalanceWithdrawal,
)
from app.shared.bases.base_model import paginate
from app.shared.bases.base_response import (
    AgentQuotaExceeded,
    AuthenticationScopeMismatch,
    NoUserBalanceObject,
    QuotaNotUpdated,
)
from app.shared.middleware.auth import JWTBearer
from app.shared.schemas.ResponseSchemas import BaseResponse

router = APIRouter(
    prefix="/api/credit",
    dependencies=[Depends(JWTBearer())],
    tags=["credit"],
)

logger = logging.getLogger("credit")
logger.addHandler(logging.StreamHandler())


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

    admin = Admin.read(id=request.user.id)
    balance = Balance.read(ownerId=context.ownerId)

    if not balance:
        return NoUserBalanceObject(success=False)

    if agent := Agent.read(id=request.user.id):
        if not agent or admin:
            return AuthenticationScopeMismatch(success=False)

        if agent.quota.balance < context.balance:
            return AgentQuotaExceeded(success=False)

        _agent_updated = Agent.update(
            id=agent.id, quota=agent.quota.balance - context.balance
        )

    _updated = Balance.update(**context.dict())
    return UpdateUserCreditResponse(success=True, response=_updated)


@router.post("/manage/update_agent_quota", response_model=UpdateAgentQuotaResponse)
async def update_agent_quota(context: UpdateAgentQuota, request: Request):
    """
    `update_agent_quota` updates the quota of an agent
    :param context: UpdateAgentQuota
    :param request: Request
    :return:  UpdateAgentQuotaResponse
    """
    _updated = Quota.update(agentId=context.agentId, balance=context.quota.balance)
    return (
        UpdateAgentQuotaResponse(success=True, response=_updated)
        if _updated
        else QuotaNotUpdated(success=False)
    )


@router.post("/manage/deposit", response_model=DepositResponse)
async def deposit(context: BalanceDeposit, request: Request):
    """
    `deposit` deposits money into a user's account
    :param context: contains the ownerId and the amount to deposit
    :param request: Request object
    :return: UpdateUserCreditResponse
    """
    if (
        _ := Deposit.where(ownerId=context.ownerId)
        .join(Status, isouter=True)
        .filter(Status.approval == "pending")
        .first()
    ):
        return BaseResponse(success=False, error="User has pending deposit")
    _status = Status.create(approval="pending")
    if not _status:
        return BaseResponse(success=False, error="Could not create withdrawal request")
    _deposit = Deposit.create(
        statusId=_status.id, ownerId=context.ownerId, amount=int(context.amount)
    )
    return UpdateUserCreditResponse(success=True, response=_deposit)


@router.post("/manage/approve_deposit", response_model=ChangeDepositStatusResponse)
async def approve_deposit(context: GetDeposit, request: Request):
    """
    `approve_deposit` approves a deposit request
    :param context: contains the ownerId and the amount to deposit
    :param request: Request object
    :return: UpdateUserCreditResponse
    """
    _deposit = Deposit.read(**context.dict(exclude_unset=True, exclude_none=True))
    if not _deposit:
        return BaseResponse(success=False, error="Deposit not found")
    _Status = Status.update(
        id=_deposit.status.id, status="approved", approvedBy=request.user.id
    )
    if not _Status:
        return BaseResponse(success=False, error="Could not approve deposit")
    _updated = Balance.update(
        ownerId=_deposit.ownerId,
        balance=_deposit.balance + _deposit.owner.balance.balance,
    )
    return ChangeDepositStatusResponse(success=True, response=_updated)


@router.post("/manage/reject_deposit", response_model=ChangeDepositStatusResponse)
async def reject_deposit(context: GetDeposit, request: Request):
    """
    `reject_deposit` rejects a deposit request
    :param context: contains the ownerId and the amount to deposit
    :param request: Request object
    :return: UpdateUserCreditResponse
    """
    _deposit = Deposit.read(**context.dict(exclude_unset=True, exclude_none=True))
    if not _deposit:
        return BaseResponse(success=False, error="Deposit not found")
    _Status = Status.update(
        id=_deposit.status.id, status="rejected", approvedBy=request.user.id
    )
    return (
        ChangeDepositStatusResponse(success=True, response=_deposit)
        if _Status
        else BaseResponse(success=False, error="Could not reject deposit")
    )


@router.post("/manage/withdraw", response_model=WithdrawalResponse)
async def withdraw(context: BalanceWithdrawal, request: Request):
    """
    `withdraw` withdraws money from a user's account
    :param context: contains the ownerId and the amount to withdraw
    :param request: Request object
    :return: UpdateUserCreditResponse
    """
    if (
        _ := Withdrawal.where(ownerId=context.ownerId)
        .join(Status, isouter=True)
        .filter(Status.approval == "pending")
        .first()
    ):
        return BaseResponse(success=False, error="User has pending withdrawal")
    _status = Status.create(approval="pending")
    if not _status:
        return BaseResponse(success=False, error="Could not create withdrawal request")
    _withdraw = Withdrawal.create(
        statusId=_status.id, ownerId=context.ownerId, amount=context.amount
    )
    return WithdrawalResponse(success=True, response=_withdraw)


@router.post("/manage/approve_withdraw", response_model=ChangeWithdrawalStatusResponse)
async def approve_withdraw(context: GetWithdrawal, request: Request):
    """
    `approve_withdraw` approves a withdrawal request
    :param context: contains the ownerId and the amount to withdraw
    :param request: Request object
    :return: UpdateUserCreditResponse
    """
    context_data = context.dict(exclude_unset=True, exclude_none=True)
    approval = context_data.pop("approvedById", None)
    _withdraw = Withdrawal.read(**context_data)
    if not _withdraw:
        return BaseResponse(success=False, error="Withdrawal not found")
    _status = Status.update(
        id=_withdraw.status.id, approval="approved", approvedById=approval
    )
    if not _status:
        return BaseResponse(success=False, error="Could not approve withdrawal")
    _updated_balance = Balance.update(
        ownerId=context.ownerId, balance=Balance.balance - _withdraw.amount
    )
    response = MakeWithdrawal(
        **dict(withdrawal=_withdraw, status=_status, balance=_updated_balance)
    )
    return ChangeWithdrawalStatusResponse(success=True, response=response)


@router.post("/manage/reject_withdraw", response_model=ChangeWithdrawalStatusResponse)
async def reject_withdraw(context: GetWithdrawal, request: Request):
    context_data = context.dict(exclude_unset=True, exclude_none=True)
    approved_id = context_data.pop("approvedById", None)
    _withdraw = Withdrawal.read(**context_data)
    if not _withdraw:
        return BaseResponse(success=False, error="Withdrawal not found")
    _Status = Status.update(
        id=_withdraw.status.id, approval="rejected", approvedById=approved_id
    )
    return (
        ChangeWithdrawalStatusResponse(success=True, response=_withdraw)
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

    filters = dict(
        status___approval=context.context.filter.status.approval,
        status___approvedById=context.context.filter.status.approvedById,
    )
    filters = {k: v for k, v in filters.items() if v}
    if context.context.filter.status.approval == "all":
        filters.pop("status___approval")
        filters.update(status___approval__in=["approved", "rejected", "pending"])
    withdrawals = Withdrawal.get_user_withdrawals(**context.params.dict(), **filters)
    return (
        GetUserWithdrawalsResponse(success=True, response=withdrawals)
        if withdrawals
        else BaseResponse(success=False, error="Withdrawals not found")
    )


@router.post("/manage/get_user_deposits", response_model=GetUserDepositsResponse)
async def get_user_deposits(context: GetUserDeposits, request: Request):
    """
    `get_user_deposits` gets all the deposits for a user
    :param context: GetUserDeposits
    :param request: Request
    :return: GetUserDepositsResponse
    """
    filters = dict(
        status___approval=context.context.filter.status.approval,
        email=context.context.filter.email,
        approvedById=context.context.filter.status.approvedById,
    )
    filters = {k: v for k, v in filters.items() if v}

    deposits = paginate(
        Deposit.where(**filters), context.params.page, context.params.size
    )
    return (
        GetUserDepositsResponse(success=True, response=deposits)
        if deposits
        else BaseResponse(success=False, error="Deposits not found")
    )
