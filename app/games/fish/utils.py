"""
@author: Kuro
@github: slapglif
"""


from app.api.user.models import User
from app.games.fish.models import Bullet
from app import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def validate_client_action(func):
    def wrapper(self, bullet_id, owner_id, bet_amount):
        user = User.read(id=owner_id)  # assuming User model exists
        if not user or user.balance < bet_amount:
            return {"success": False}
        bullet = Bullet.read(id=bullet_id)  # assuming Bullet model exists
        if bullet:
            return {"success": False}
        return func(self, bullet_id, owner_id, bet_amount)

    return wrapper


def handle_fish_hit(func):
    def wrapper(self, fish_id):
        try:
            result = func(self, fish_id)
            if not result.get("success"):
                logging.warning(f"Server-side fish hit failed for fish_id={fish_id}")
            return result
        except Exception as e:
            logging.exception(f"Unexpected error during server-side fish hit: {e}")
            return {"success": False}

    return wrapper
