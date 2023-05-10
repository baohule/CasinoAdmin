"""
@author: Kuro
"""
from datetime import datetime
from enum import Enum
from typing import Optional, Union, List, Dict
from uuid import UUID

from fastapi_camelcase import CamelModel
from pydantic import Field

from app.api.agent.schema import AgentQuota
from app.shared.schemas.ResponseSchemas import BaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel
from app.shared.schemas.page_schema import GetOptionalContextPages, Filter, PagedResponse


class User(ORMCamelModel):
    id: Optional[int]
    phone: Optional[str]
    username: Optional[str]


class UserCredit(ORMCamelModel):
    """
    `UserCredit` is a class that is used to represent a user credit
    """

    id: Optional[UUID]
    timestamp: Optional[str]
    balance: float = Field(default=0)
    owner: Optional[User]


class GetUserCredit(CamelModel):
    """
    `GetUserCredit` is a class that is used to represent a request
    """

    ownerId: int


class GetUserCreditResponse(BaseResponse):
    """
    `GetUserCreditResponse` is a class that is used to represent a response
    """

    response: Optional[UserCredit]


class UpdateUserCredit(CamelModel):
    """
    `UpdateUserCredit` is a class that is used to represent a request
    """

    ownerId: int
    balance: float


class UpdateUserCreditResponse(BaseResponse):
    """
    `UpdateUserCreditResponse` is a class that is used to represent a response
    """

    response: Optional[UserCredit]


class DeleteUserCredit(CamelModel):
    """
    `DeleteUserCredit` is a class that is used to represent a request
    """

    id: int


class DeleteUserCreditResponse(BaseResponse):
    """
    `DeleteUserCreditResponse` is a class that is used to represent a response
    """

    response: Optional[UUID]


class CreateUserCredit(CamelModel):
    """
    `CreateUserCredit` is a class that is used to represent a request
    """

    balance: float
    ownerId: int


class CreateUserCreditResponse(BaseResponse):
    """
    `CreateUserCreditResponse` is a class that is used to represent a response
    """

    response: Optional[UserCredit]


class AgentQuta(ORMCamelModel):
    """
    `AgentQuta` is a class that is used to represent a user credit
    """
    id: Optional[UUID]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    balance: Optional[float]


class UpdateAgentQuotaResponse(BaseResponse):
    """
    `UpdateAgentQuotaResponse` is a class that is used to represent a response
    """

    response: Optional[AgentQuta]


class UpdateAgentQuota(CamelModel):
    """
    `UpdateAgentQuota` is a class that is used to represent a request
    """

    agentId: UUID
    quota: AgentQuota


class Status(ORMCamelModel):
    """
    `Approval` is a class that is used to represent a user approval
    """

    approvedById: Optional[UUID]
    approval: Optional[str] = Field(default=None)


class MakeDeposit(ORMCamelModel):
    """
    `Deposit` is a class that is used to represent a user deposit
    """

    id: Optional[UUID]
    amount: Optional[int]
    owner: Optional[User]
    status: Optional[Status]


class BalanceDeposit(CamelModel):
    """
    `BalanceDeposit` is a class that is used to represent a request
    """

    ownerId: Optional[int]
    amount: Optional[int]


class BalanceWithdrawal(CamelModel):
    """
    `BalanceWithdrawal` is a class that is used to represent a request
    """

    ownerId: Optional[int]
    amount: Optional[int]


class DepositResponse(BaseResponse):
    """
    `Deposit` is a class that is used to represent a user deposit
    """

    response: Optional[MakeDeposit]


class MakeWithdrawal(ORMCamelModel):
    """
    `Withdrawal` is a class that is used to represent a user withdrawal
    """

    id: Optional[UUID]
    amount: Optional[int]
    owner: Optional[User]
    status: Optional[Status]


class GetWithdrawal(CamelModel):
    """
    `GetWithdrawal` is a class that is used to represent a request
    """

    ownerId: Optional[int] = Field(default=None, description="optional")
    id: Optional[UUID] = Field(default=None, description="optional")
    approvedById: Optional[UUID] = Field(default=None, description="optional")


class GetDeposit(CamelModel):
    """
    `GetDeposit` is a class that is used to represent a request
    """

    ownerId: Optional[int] = Field(default=None, description="optional")
    id: Optional[UUID] = Field(default=None, description="optional")
    approvedById: Optional[UUID] = Field(default=None, description="optional")



class ApproveDeposit(CamelModel):
    """
    `ApproveDeposit` is a class that is used to represent a request
    """
    id: Optional[UUID]
    approvedById: Optional[UUID]


class ApproveWithdrawal(CamelModel):
    """
    `ApproveWithdrawal` is a class that is used to represent a request
    """

    id: Optional[UUID]
    approvedById: Optional[UUID]


class ChangeDepositStatusResponse(BaseResponse):
    """
    `ApproveDepositResponse` is a class that is used to represent a response
    """

    response: Optional[MakeDeposit]


class ChangeWithdrawalStatusResponse(BaseResponse):
    """
    `ApproveWithdrawalResponse` is a class that is used to represent a response
    """

    response: Optional[MakeWithdrawal]


class WithdrawalResponse(BaseResponse):
    """
    `Withdrawal` is a class that is used to represent a user withdrawal
    """

    response: Optional[MakeWithdrawal]


class WithdrawalContext(CamelModel):
    """
    `WithdrawalContext` is a class that is used to represent a context
    """
    status: Optional[Status] = Field(default=None, description="optional")


class WithdrawalFilter(Filter):
    """
    `WithdrawalFilter` is a class that is used to represent a filter
    """

    filter: Optional[WithdrawalContext]


class GetUserDepositPages(PagedResponse):
    """
    `GetUserDepositPages` is a class that is used to represent a request
    """

    items: Optional[List[MakeDeposit]]


class GetUserWithdrawalPages(PagedResponse):
    """
    `GetUserWithdrawalPages` is a class that is used to represent a request
    """

    items: Optional[List[MakeWithdrawal]]


class GetUserDepositsResponse(BaseResponse):
    """
    `GetUserWithdrawalsResponse` is a class that is used to represent a response
    """

    response: Optional[GetUserDepositPages]


class GetUserWithdrawalsResponse(BaseResponse):
    """
    `GetUserWithdrawalsResponse` is a class that is used to represent a response
    """

    response: Optional[GetUserWithdrawalPages]


class DepositContext(CamelModel):
    """
    `WithdrawalContext` is a class that is used to represent a context
    """
    phone: Optional[str]
    status: Optional[Status]


class DepositFilter(Filter):
    """
    `WithdrawalFilter` is a class that is used to represent a filter
    """

    filter: Optional[DepositContext]


class GetUserDeposits(GetOptionalContextPages):
    """
    `GetUserWithdrawals` is a class that is used to represent a request
    """

    context: Optional[DepositFilter]


class GetUserWithdrawals(GetOptionalContextPages):
    """
    `GetUserWithdrawals` i
    s a class that is used to represent a request
    """

    context: Optional[WithdrawalFilter]
