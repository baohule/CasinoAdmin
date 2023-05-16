"""
@author: Kuro
@github: slapglif
"""
import random
from typing import Dict, List, Optional
from random import randint, seed

import schedule as schedule
from py_linq import Enumerable
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.game.models import Fish, Paths
from app.api.user.models import User
from app.games.fish.models import GameResult, Bullet
from app.rpc.fish_game import GameConfig
from app.shared.schemas.ResponseSchemas import BaseResponse


# SQLAlchemy models (assumed to exist)
# User, GameSession, Fish, Bullet, GameResult, GameConfig

class FishGame:
    """
    Fish game class that handles game logic and server-side validation.
    """
    def __init__(self, game_config: GameConfig = GameConfig()):
        # Initialize game config values from database

        # Initialize reward pool and total bet to zero
        self.reward_pool = 0
        self.total_bet = 0
        self.fish_pool = []
        # Initialize big win flag to false
        self.big_win = False
        self.paths = game_config.paths
        self.taken_paths = []
        schedule.every(3).seconds.do(self.fish_out)

    def shoot_fish(self, user: User, bet_amount: int) -> BaseResponse:
        """
        Validates client action by checking if bullet ID is already in use
        and if user has enough balance to place the bet.
        """

        if not user:
            return BaseResponse(error="User not found")
        if user.creditAccount.balance < bet_amount:
            return BaseResponse(error="Insufficient balance")
        # if bullet_id := Bullet.read(id=bullet_id):
            # return BaseResponse(error="Bullet ID already in use")
        player_session = user.userSessions[-1]
        bullet = Bullet.create(
            bet=100,
            player_session_id=player_session.id
        )
        bullet.save()
        user.creditAccount.balance -= bet_amount
        user.save()
        # Deprecated because bullet is created at the time
        # of the shoot event, adding it to the list automatically
        # self.append_bullet_list(bullet_id, bet_amount, owner=user)
        return BaseResponse(success=True)

    def fish_hit(self, bullet_id: int, owner: User, fish_id: int) -> BaseResponse:
        """
        Checks if fish is hit (according to probability distribution)
        and updates game result accordingly.
        """
        bullet = Bullet.read(id=bullet_id)
        for fish in self.fish_pool:
            if fish["fish_id"] == fish_id and bullet:
                if kill := self.get_prob_distribution(fish.difficulty):
                    reward = fish.coin  # use coin field as reward amount
                    session = owner.userSessions[-1]
                    game_result = GameResult(player_session_id=session.id, bullet_id=bullet_id, win=reward)
                    game_result.save()  # assuming save method exists for GameResult model
                    return BaseResponse(success=True)
                return BaseResponse()
            return BaseResponse()

    # @staticmethod
    # def append_bullet_list(bullet_id: int, bet_amount: int, owner: User) -> Dict[str, int]:
    #     """
    #     Adds a new bullet to the list and returns bullet information.
    #     """
    #     if not owner.userSessions:
    #         return
    #     session = Enumerable(owner.userSessions).first()
    #
    #     bullet = Bullet(id=bullet_id, bet=bet_amount, player_session_id=session.id)
    #     bullet.save()  # assuming save method exists for Bullet model

    def kill_big_fish(self, user_id: int = None, bullet_id: int = None, fish_id: int = None) -> bool:
        """
        Determines if the big fish is killed based on chance (with probability of big_win)
        and updates game result accordingly.
        """
        rtp = 0.85
        chance = self.total_bet * rtp / 100
        return self._reward(user_id, bullet_id, fish_id) if self.big_win and randint(1, 100) <= chance else False

    def _reward(self, user_id: int = None, bullet_id: int = None, fish_id: int = None ) -> bool:
        reward = sum(fish.coin for fish in GameResult.all())
        game_result = GameResult(user_id=user_id, bullet_id=bullet_id, fish_id=fish_id, win=reward)
        # Deduct winning from total bet (reward pool already increased in serverside_fish_hit)
        self.total_bet -= reward
        game_result.save()  # assuming save method exists for GameResult model
        self.big_win = False  # reset big_win flag
        return True

    @staticmethod
    def get_prob_distribution(difficulty: int) -> int:
        """
        Returns the probability distribution for hitting a fish based on its property value.
        Assumes higher property values have lower probabilities.
        """
        seeds: float = random.random()
        difficulty_level: float = difficulty / 100
        prob_range: list = [(difficulty_level - 1) * 0.05, difficulty_level * 0.05]
        return prob_range[0] <= seeds < prob_range[1]

    def fish_out(self):
        """
    The fish_out function is a method of the Pond class. It returns a random fish object from the pond,
        and it has an equal chance of returning any type of fish in the pond. The function also has a 5% chance
        to return 3-5 small fishes instead of one large fish.

    Args:
        self: Refer to the object itself

    Returns:
        A fish object
    """
        fish_type = random.randint(1, 25)
        if fish_type < 5:
            for _ in range(random.randint(3, 5)):
                return self.generate_fish(fish_type)
        return self.generate_fish(fish_type)

    def generate_fish(self, fish_type: int):
        path = random.choice(Paths.all())
        fish_data = Fish.read(fishType=fish_type)
        if path not in self.taken_paths:
            self.taken_paths.append(path)
            fish_data.path = path
            self.fish_pool.append(fish_data)


