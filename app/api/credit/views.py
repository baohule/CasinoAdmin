"""
@author: Kuro
"""
from fastapi import APIRouter, Depends, Request

from app.api.agent.models import Agent
from app.api.credit import schema
from app.api.credit.models import Balance
from app.api.credit.schema import (
    CreateUserCreditResponse,
    CreateUserCredit,
    UserCredit,
    GetUserCredit,
    GetUserCreditResponse,
    UpdateUserCreditResponse,
    UpdateUserCredit, UpdateAgentQuotaResponse, UpdateAgentQuota,
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