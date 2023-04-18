"""
@author: Kuro
"""
from datetime import datetime
from enum import Enum
from typing import Optional, Union, List, Dict
from uuid import UUID

from fastapi_camelcase import CamelModel
from pydantic import Field

from app.shared.schemas.ResponseSchemas import BaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel
from app.shared.schemas.page_schema import GetOptionalContextPages, Filter, PagedResponse


class User(ORMCamelModel):
    id: Optional[UUID]
    email: Optional[str]
    name: Optional[str]


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

    ownerId: UUID


class GetUserCreditResponse(BaseResponse):
    """
    `GetUserCreditResponse` is a class that is used to represent a response
    """

    response: Optional[UserCredit]


class UpdateUserCredit(CamelModel):
    """
    `UpdateUserCredit` is a class that is used to represent a request
    """

    ownerId: UUID
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

    id: UUID


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
    ownerId: UUID


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
    agent: Optional[User]


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
    balance: float


class ApprovalStatus(str, Enum):
    """
    `ApprovalStatus` is a class that is used to represent a user approval status
    """

    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "rejected"


class Status(ORMCamelModel):
    """
    `Approval` is a class that is used to represent a user approval
    """

    approvedById: Optional[UUID]
    approval: ApprovalStatus = Field(default=ApprovalStatus.PENDING)


class Deposit(ORMCamelModel):
    """
    `Deposit` is a class that is used to represent a user deposit
    """

    id: Optional[UUID]
    amount: float
    owner: Optional[User]
    approval: Optional[Status]


class DepositResponse(BaseResponse):
    """
    `Deposit` is a class that is used to represent a user deposit
    """

    response: Optional[Deposit]


class Withdrawal(ORMCamelModel):
    """
    `Withdrawal` is a class that is used to represent a user withdrawal
    """

    id: Optional[UUID]
    amount: float = Field(default=0)
    owner: Optional[User]
    approval: Optional[Status]


class WithdrawalResponse(BaseResponse):
    """
    `Withdrawal` is a class that is used to represent a user withdrawal
    """

    response: Optional[Withdrawal]


class WithdrawalContext(CamelModel):
    """
    `WithdrawalContext` is a class that is used to represent a context
    """
    ownerId: Optional[UUID]
    approvalStatus: Optional[ApprovalStatus]


class WithdrawalFilter(Filter):
    """
    `WithdrawalFilter` is a class that is used to represent a filter
    """

    filter: Optional[WithdrawalContext]


class GetUserDepositPages(PagedResponse):
    """
    `GetUserDepositPages` is a class that is used to represent a request
    """

    items: Optional[List[Deposit]]


class GetUserWithdrawalPages(PagedResponse):
    """
    `GetUserWithdrawalPages` is a class that is used to represent a request
    """

    items: Optional[List[Withdrawal]]


class GetUserDepositsResponse(BaseResponse):
    """
    `GetUserWithdrawalsResponse` is a class that is used to represent a response
    """

    response: GetUserDepositPages


class GetUserWithdrawalsResponse(BaseResponse):
    """
    `GetUserWithdrawalsResponse` is a class that is used to represent a response
    """

    response: GetUserWithdrawalPages


class DepositContext(CamelModel):
    """
    `WithdrawalContext` is a class that is used to represent a context
    """
    ownerId: Optional[UUID]
    approvalStatus: Optional[ApprovalStatus]


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
    `GetUserWithdrawals` is a class that is used to represent a request
    """

    context: Optional[WithdrawalFilter]
