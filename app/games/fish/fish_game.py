"""
@author: Kuro
@github: slapglif
"""
import random
from dataclasses import dataclass

from py_linq import Enumerable

import settings
from app.api.game.models import Paths, GameSession
from app.api.user.models import User
from app.games.fish.models import GameResult, BetEvent, Reward
from app.games.fish.schema import Objective

from app.shared.schemas.ResponseSchemas import BaseResponse


# SQLAlchemy models (assumed to exist)
# User, GameSession, Fish, Bullet, GameResult, GameConfig
