"""
@author: Kuro
"""
import uuid
from datetime import datetime
import pytz
from fastapi_sqlalchemy import db
from pydantic import BaseModel
from sqlalchemy import (
    Column,
    String,
    Date,
    Boolean,
    DateTime,
    Text,
    Float,
    ForeignKey,
    Integer, Enum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from app.api.user.models import User
from app.shared.bases.base_model import ModelMixin, Page
from app.shared.bases.base_model import paginate


class Balance(ModelMixin):
    """
    Balance is a table that stores the balance of a user.
    """

    __tablename__ = "Balance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    balance = Column(Integer, default=0)
    createdAt = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    updatedAt = Column(DateTime)
    ownerId = Column(
        UUID(as_uuid=True),
        ForeignKey("User.id", ondelete="CASCADE", link_to_name=True),
        index=True,
        unique=True,
    )
    credit_account = relationship(
        "User",
        foreign_keys="Balance.ownerId",
        backref=backref("creditAccount", single_parent=True, uselist=False),
    )


class Quota(ModelMixin):
    """
    Quota is a table that stores the quota of a user.
    """

    __tablename__ = "Quota"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    balance = Column(Integer, default=0)
    createdAt = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    updatedAt = Column(DateTime)
    agentId = Column(
        UUID(as_uuid=True),
        ForeignKey("Agent.id", ondelete="CASCADE", link_to_name=True),
        index=True,
        unique=True,
    )
    agent_quota = relationship(
        "Agent",
        foreign_keys="Quota.agentId",
        backref=backref("agentQuota", single_parent=True, uselist=False),
    )


class StatusEnum(str, Enum):
    """
    Status is a table that stores the status of a user.
    """
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Status(ModelMixin):
    """
    Approval is a table that stores the approval of a user.
    """

    __tablename__ = "Status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    createdAt = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    updatedAt = Column(DateTime)
    approval = Column(Text, default="pending")
    approvedById = Column(
        UUID(as_uuid=True),
        ForeignKey("Agent.id", ondelete="CASCADE", link_to_name=True),
        index=True,
        nullable=True
    )
    approvedBy = relationship(
        "Agent",
        foreign_keys="Status.approvedById",
        backref=backref("approvedBy", single_parent=True, uselist=False),
    )


class Withdrawal(ModelMixin):
    """
    Withdrawal is a table that stores the withdrawal of a user.
    """

    __tablename__ = "Withdrawal"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    amount = Column(Integer)
    createdAt = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    updatedAt = Column(DateTime)
    statusId = Column(
        UUID(as_uuid=True),
        ForeignKey("Status.id", ondelete="CASCADE", link_to_name=True),
        index=True,
    )
    status = relationship(
        "Status",
        foreign_keys="Withdrawal.statusId",
        backref=backref("withdrawalStatus", single_parent=True, uselist=False),
    )
    ownerId = Column(
        UUID(as_uuid=True),
        ForeignKey("User.id", ondelete="CASCADE", link_to_name=True),
        index=True,
    )
    owner = relationship(
        "User",
        foreign_keys="Withdrawal.ownerId",
        backref=backref("userWithdrawals", single_parent=True, uselist=False),
    )


class Deposit(ModelMixin):
    """
    Deposit is a table that stores the deposit of a user.
    """

    __tablename__ = "Deposit"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    amount = Column(Integer)
    createdAt = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    updatedAt = Column(DateTime)
    statusId = Column(
        UUID(as_uuid=True),
        ForeignKey("Status.id", ondelete="CASCADE", link_to_name=True),
        index=True,
    )
    status = relationship(
        "Status",
        foreign_keys="Deposit.statusId",
        backref=backref("depositStatus", single_parent=True, uselist=False),
    )
    ownerId = Column(
        UUID(as_uuid=True),
        ForeignKey("User.id", ondelete="CASCADE", link_to_name=True),
        index=True,
    )
    owner = relationship(
        "User",
        foreign_keys="Deposit.ownerId",
        backref=backref("userDeposits", single_parent=True, uselist=False),
    )
