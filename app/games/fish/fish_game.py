"""
@author: Kuro
@github: slapglif
"""


from typing import Dict, List, Optional
from random import randint, seed
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.game.models import Fish
from app.api.user.models import User
from app.games.fish.models import GameResult, Bullet
from app.rpc.fish_game import GameConfig


# SQLAlchemy models (assumed to exist)
# User, GameSession, Fish, Bullet, GameResult, GameConfig



class FishGame:
    def __init__(self, session: Session):
        # Initialize game config values from database
        self.difficulty = session.query(GameConfig).first().difficulty
        self.rtp = session.query(GameConfig).first().rtp
        self.seed_value = session.query(GameConfig).first().seed_value

        # Set seed value for deterministic pseudo-random number generation
        seed(self.seed_value)

        # Initialize reward pool and total bet to zero
        self.reward_pool = 0
        self.total_bet = 0

        # Initialize big win flag to false
        self.bigwin = False

    def validate_client_action(self, bullet_id: int, owner_id: int, bet_amount: int) -> Dict[str, bool]:
        """
        Validates client action by checking if bullet ID is already in use
        and if user has enough balance to place the bet.
        """
        user = User.read(id=owner_id)  # assuming User model exists
        if not user:
            return {"success": False}
        if user.balance < bet_amount:
            return {"success": False}
        if bullet := Bullet.read(id=bullet_id):
            return {"success": False}
        return {"success": True}

    def fish_hit(self, bullet_id: int, owner_id: int, fish_id: int) -> Optional[Dict[str, bool]]:
        """
        Checks if fish is hit (according to probability distribution)
        and updates game result accordingly.
        """
        fish = Fish.session.query(Fish).get(fish_id)  # assuming Fish model exists and session is provided
        if not fish:
            return None
        prob_dist = self.get_prob_distribution(fish.propValue)  # assumes get_prob_distribution is defined
        hit = randint(1, 100) <= prob_dist
        if hit:
            reward = fish.coin  # use coin field as reward amount
            game_result = GameResult(user_id=owner_id, bullet_id=bullet_id, fish_id=fish_id, win=reward)
            # Deduct winning from total bet (reward pool already increased in serverside_fish_hit)
            self.total_bet -= reward
            game_result.save()  # assuming save method exists for GameResult model
            return {"success": True}
        else:
            return {"success": False}

    def server_side_fish_hit(self, fish_id: int) -> Dict[str, bool]:
        """
        'Hits' the fish on the server side by adding the bet amount to the reward pool
        and total bet, and returning updated fish information.
        """
        fish = Fish.session.query(Fish).get(fish_id)  # assuming Fish model exists and session is provided
        if not fish:
            return {"success": False}
        self.reward_pool += fish.prop  # use prop field as bet amount
        self.total_bet += fish.prop
        updated_fish = {"fish_id": fish_id, "new_reward_pool": self.reward_pool, "new_total_bet": self.total_bet}
        return {"success": True, "updated_fish": updated_fish}

    def append_bullet_list(self, bullet_id: int, bet_amount: int, owner_id: int) -> Dict[str, int]:
        """
        Adds a new bullet to the list and returns bullet information.
        """
        bullet = Bullet(id=bullet_id, bet=bet_amount, user_id=owner_id)
        bullet.save()  # assuming save method exists for Bullet model
        return {"bullet_id": bullet_id, "bet_amount": bet_amount, "owner_id": owner_id}

    def fishout(self) -> List[Dict[str, int]]:
        """
        Returns information about all the available fish in the game.
        """
        fishes = Fish.session.query(Fish).all()
        return [{"fish_id": fish.id, "fish_type": fish.fishType} for fish in fishes]

    def bigfish_chance(self) -> float:
        """
        Returns the chance to kill a big fish based on total bet and RTP (Return to player percentage).
        """
        return self.total_bet * self.rtp / 100

    def kill_big_fish(self) -> bool:
        """
        Determines if the big fish is killed based on chance (with probability of bigwin)
        and updates game result accordingly.
        """
        if self.bigwin and randint(1, 100) <= self.bigfish_chance():
            reward = sum(fish.coin for fish in GameResult.session.query(Fish).all())
            game_result = GameResult(user_id=None, bullet_id=None, fish_id='big_fish', win=reward)
            # Deduct winning from total bet (reward pool already increased in serverside_fish_hit)
            self.total_bet -= reward
            game_result.save()  # assuming save method exists for GameResult model
            self.bigwin = False  # reset bigwin flag
            return True
        else:
            return False

    def get_prob_distribution(self, prop_value: float) -> int:
        """
        Returns the probability distribution for hitting a fish based on its property value.
        Assumes higher property values have lower probabilities.
        """
        if prop_value >= 0.7:
            return 80
        elif 0.4 <= prop_value < 0.7:
            return 60
        elif 0.2 <= prop_value < 0.4:
            return 40
        elif 0.1 <= prop_value < 0.2:
            return 20
        else:
            return 10
        #