"""
@author: Kuro
@github: slapglif
"""
from datetime import datetime

import pytz
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import null
from app.shared.bases.base_model import ModelMixin

class GameResult(ModelMixin):
    __tablename__ = "GameResult"

    id = Column(Integer, primary_key=True, index=True)
    player_session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("PlayerSession.id", ondelete="CASCADE", link_to_name=True),
        index=True,
        nullable=True,
    )
    player_session = relationship(
        "PlayerSession",
        foreign_keys="GameResult.player_session_id",
        backref=backref("game_result", single_parent=True),
    )
    bullet_id = Column(
        Integer,
        ForeignKey("Bullet.id", ondelete="CASCADE", link_to_name=True),
        index=True,
        nullable=True,
    )
    # bullet_id = Column(Integer, ForeignKey("Bullet.id"))
    # fish_id = Column(Integer, ForeignKey("Fish.id"))
    win = Column(Integer)
    #
    # bullet = relationship("Bullet", back_populates="GameResult")
    # fish = relationship("Fish", back_populates="GameResult")
    #


class Bullet(ModelMixin):
    __tablename__ = "Bullet"

    id = Column(Integer, primary_key=True, index=True)
    bet = Column(Integer)
    player_session_id = Column(UUID(as_uuid=True), ForeignKey("PlayerSession.id"))
    createdAt = Column(DateTime, default=lambda: datetime.now(pytz.utc))

    #player_session = relationship("User", back_populates="User")
    #game_results = relationship("GameResult", back_populates="GameResult")
