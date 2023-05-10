import uuid
from random import random

from alembic.seeders.seed_fish_data import fish_config
from app.rpc.fish_game import FishGame, game_config, User
from pydantic import BaseModel


class BulletData(BaseModel):
    bullet_id: uuid.uuid4()
    owner_id: uuid.uuid4()
    bet: int


class FishInfo(BaseModel):
    fish_id: uuid.uuid4()
    fish_type: int
    fish_coin: int


class Pay(FishGame):
    def __init__(self):
        self.fish_config = fish_config
        self.game_config = game_config
        self.reward_pool: int = 0
        self.bullet_pool = []

    def shoot(self, data: dict):
        user = User(**data['user'])
        bet = int(data['bet'])
        user.credits -= bet
        self.reward_pool += bet
        self.bullet_pool.append(
            BulletData(bullet_id=uuid.uuid4(), owner_id=user.id, bet=bet)
        )
        return None

    def fish_hit(self, data):
        user = User(**data['user'])
        fish_data = FishInfo(**data['fish'])
        fish_id = fish_data.fish_id

        target_fish = self.fishList[user.table_id][fish_id].getfish_type()
        is_kill = self.compute_probability(fish_data.fish_type)
        if target_fish < 0 or target_fish >= len(self.fish_config) \
                or not self.fishList[user.table_id].get(fish_id) \
                or self.fishList[user.table_id][fish_id].getfish_id() != fish_id \
                or self.fishList[user.table_id][fish_id].isDel() \
                or not is_kill:
            return {'score': 0, 'propId': 0, 'propCount': 0}
        return {'userId': user.id, 'score': fish_data.fish_coin, 'fish_id': fish_id, 'propId': 0, 'propCount': 0}

    def compute_probability(self, fish_type: int):
        seed: float = random.random()
        difficulty_level: int = self.fish_config[fish_type].difficulty
        prob_range: list = [(difficulty_level - 1) * 0.05, difficulty_level * 0.05]
        if prob_range[0] <= seed < prob_range[1]:
            return True
        return False

