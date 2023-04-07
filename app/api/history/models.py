"""
@author: Kuro
"""
import uuid
from datetime import datetime

import pytz
from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from app import ModelMixin


class PaymentHistory(ModelMixin):
    """
    PaymentHistory is a table that stores the payment history of a user.
    """

    __tablename__ = "PaymentHistory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    beforeScore = Column(Integer)
    changeScore = Column(Integer)
    newScore = Column(Integer)
    approval = Column(Boolean)
    createdAt = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    approvalAt = Column(DateTime)
    ownerId = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "user.id",
            ondelete="CASCADE",
            link_to_name=True,
        ),
        index=True,
    )
    owner = relationship(
        "User",
        foreign_keys="PaymentHistory.ownerId",
        backref=backref("paymentHistory", single_parent=True),
    )


class BetDetailHistory(ModelMixin):
    """
    BetDetailHistory is a table that stores the
    history of bet details performed by users
    """

    __tablename__ = "BetDetailHistory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    beforeScore = Column(Integer)
    betScore = Column(Integer)
    winScore = Column(Integer)
    newScore = Column(Integer)
    updateAt = Column(DateTime)
    createdAt = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    gameId = Column(
        Integer,
        ForeignKey("game_list.id", ondelete="CASCADE", link_to_name=True),
        index=True,
    )
    game = relationship(
        "GameList",
        foreign_keys="BetDetailHistory.gameId",
        backref=backref("game", single_parent=True, uselist=False),
    )
    ownerId = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE", link_to_name=True),
        index=True,
    )
    owner = relationship(
        "User",
        foreign_keys="BetDetailHistory.ownerId",
        backref=backref("betHistory", single_parent=True),
    )


class ActionHistory(ModelMixin):
    """
    ActionHistory is a table that stores the history
    of actions performed by users, agents, and admins

    """

    __tablename__ = "ActionHistory"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    newValueJson = Column(JSON)
    ip = Column(String(255), nullable=False)
    createdAt = Column(DateTime)
    userId = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE", link_to_name=True),
        index=True,
        nullable=True,
    )
    userActionHistory = relationship(
        "User",
        foreign_keys="ActionHistory.userId",
        backref=backref("userActionHistory", single_parent=True),
    )
    agentId = Column(
        UUID(as_uuid=True),
        ForeignKey("agent.id", ondelete="CASCADE", link_to_name=True),
        index=True,
        nullable=True,
    )
    agentActionHistory = relationship(
        "Agent",
        foreign_keys="ActionHistory.agentId",
        backref=backref("agentActionHistory", single_parent=True),
    )
    adminId = Column(
        UUID(as_uuid=True),
        ForeignKey("admin.id", ondelete="CASCADE", link_to_name=True),
        index=True,
        nullable=True,
    )
    adminActionHistory = relationship(
        "Admin",
        foreign_keys="ActionHistory.adminId",
        backref=backref("adminActionHistory", single_parent=True),
    )
