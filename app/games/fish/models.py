"""
@author: Kuro
@github: slapglif
"""



from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from app.shared.bases.base_model import ModelMixin

class GameResult(ModelMixin):
    __tablename__ = "game_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bullet_id = Column(Integer, ForeignKey("bullets.id"))
    fish_id = Column(Integer, ForeignKey("fish.id"))
    win = Column(Integer)

    user = relationship("User", back_populates="game_results")
    bullet = relationship("Bullet", back_populates="game_results")
    fish = relationship("Fish", back_populates="game_results")



class Bullet(ModelMixin):
    __tablename__ = "bullets"

    id = Column(Integer, primary_key=True, index=True)
    bet = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="bullets")
    game_results = relationship("GameResult", back_populates="bullet")
