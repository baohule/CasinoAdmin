"""
@author: Kuro
@github: slapglif
"""
import random
from typing import Dict, List, Optional
from random import randint, seed

import schedule as schedule
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.game.models import Fish, Paths
from app.api.user.models import User
from app.games.fish.models import GameResult, Bullet
from app.rpc.fish_game import GameConfig


# SQLAlchemy models (assumed to exist)
# User, GameSession, Fish, Bullet, GameResult, GameConfig

class FishGame:
    """
    Fish game class that handles game logic and server-side validation.
    """
    def __init__(self, session: Session):
        # Initialize game config values from database

        # Initialize reward pool and total bet to zero
        self.reward_pool = 0
        self.total_bet = 0
        self.fish_pool = []
        # Initialize big win flag to false
        self.big_win = False
        self.paths = session.query(GameConfig).first()
        self.taken_paths = []
        schedule.every(3).seconds.do(self.fish_out)

    def shoot_fish(self, bullet_id: int, owner_id: int, bet_amount: int) -> Dict[str, bool]:
        """
        Validates client action by checking if bullet ID is already in use
        and if user has enough balance to place the bet.
        """
        user = User.read(id=owner_id)  # assuming User model exists
        if not user:
            return {"success": False}
        if user.balance < bet_amount:
            return {"success": False}
        if bullet_id := Bullet.read(id=bullet_id):
            return {"success": False}
        return {"success": True}

    def fish_hit(self, bullet_id: int, owner_id: int, fish_id: int) -> Optional[Dict[str, bool]]:
        """
        Checks if fish is hit (according to probability distribution)
        and updates game result accordingly.
        """
        for fish in self.fish_pool:
            if fish["fish_id"] == fish_id:
                hit = self.get_prob_distribution(fish.difficulty)  # assumes difficulty is defined
                if hit:
                    reward = fish.coin  # use coin field as reward amount
                    game_result = GameResult(user_id=owner_id, bullet_id=bullet_id, fish_id=fish_id, win=reward)
                    # Deduct winning from total bet (reward pool already increased in serverside_fish_hit)
                    self.total_bet -= reward
                    game_result.save()  # assuming save method exists for GameResult model
                    return {"success": True}
                else:
                    return {"success": False}
            return None

    def append_bullet_list(self, bullet_id: int, bet_amount: int, owner_id: int) -> Dict[str, int]:
        """
        Adds a new bullet to the list and returns bullet information.
        """
        bullet = Bullet(id=bullet_id, bet=bet_amount, user_id=owner_id)
        bullet.save()  # assuming save method exists for Bullet model
        return {"bullet_id": bullet_id, "bet_amount": bet_amount, "owner_id": owner_id}

    def kill_big_fish(self) -> bool:
        """
        Determines if the big fish is killed based on chance (with probability of bigwin)
        and updates game result accordingly.
        """
        rtp = 0.85
        chance = self.total_bet * rtp / 100
        if self.big_win and randint(1, 100) <= chance:
            reward = sum(fish.coin for fish in GameResult.session.query(Fish).all())
            game_result = GameResult(user_id=None, bullet_id=None, fish_id='big_fish', win=reward)
            # Deduct winning from total bet (reward pool already increased in serverside_fish_hit)
            self.total_bet -= reward
            game_result.save()  # assuming save method exists for GameResult model
            self.bigwin = False  # reset bigwin flag
            return True
        else:
            return False

    def get_prob_distribution(self, difficulty: int) -> int:
        """
        Returns the probability distribution for hitting a fish based on its property value.
        Assumes higher property values have lower probabilities.
        """
        seeds: float = random.random()
        difficulty_level: float = difficulty / 100
        prob_range: list = [(difficulty_level - 1) * 0.05, difficulty_level * 0.05]
        if prob_range[0] <= seeds < prob_range[1]:
            return True
        return False

    def fish_out(self):
        fish_type = random.randint(1, 25)
        if fish_type < 5:
            for _ in range(random.randint(3, 5)):
                return self.generate_fish(fish_type)
        return self.generate_fish(fish_type)

    def generate_fish(self, fish_type: int):
        path = random.choice(Paths.all)
        fish_data = Fish.session.query().read(fishType=fish_type)
        if path not in self.taken_paths:
            self.taken_paths.append(path)
            fish_data.path = path
            self.fish_pool.append(fish_data)


