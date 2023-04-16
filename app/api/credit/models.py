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
    Integer,
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
    balance = Column(Integer)
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