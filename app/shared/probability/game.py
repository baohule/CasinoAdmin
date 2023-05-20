import random

from dataclasses import dataclass
from py_linq import Enumerable

import settings
from app.api.game.models import Paths, GameSession
from app.api.user.models import User
from app.games.fish.models import GameResult, BetEvent, Reward
from app.games.fish.schema import Objective
from app.rpc.game.schema import Session
from app.shared.schemas.ResponseSchemas import BaseResponse


@dataclass
class GameProbability:
    """
    Fish game class that handles game logic and server-side validation.
    """

    session = Session
    reward_pool: list
    total_bet: int
    big_win: bool
    paths: Paths
    taken_paths: list
    rtp_pool_max: float = settings.Config.rtp_pool_max
    rtp_user_min: int = settings.Config.rtp_user_min

    @classmethod
    def initiate_bet(cls, user: User, bet_amount: int) -> BaseResponse:
        """
        Validates client action by checking if bullet ID is already in use
        and if user has enough balance to place the bet.
        """

        if not user:
            return BaseResponse(error="User not found")
        if user.balance.amount < bet_amount:
            return BaseResponse(error="Insufficient balance")
        # if bullet_id := Bullet.read(id=bullet_id):
        # return BaseResponse(error="Bullet ID already in use")
        player_session = user.userSessions[-1]
        event = BetEvent.create(bet=bet_amount, player_session_id=player_session.id)
        event.save()
        user.balance.amount -= bet_amount
        user.rtp += bet_amount
        user.save()

        # Deprecated because bullet is created at the time
        # of the shoot event, adding it to the list automatically
        # self.append_bullet_list(bullet_id, bet_amount, owner=user)
        return BaseResponse(success=True, response=event.id)

    @classmethod
    def bet_close(cls, event: BetEvent, user: User, reward_id: int) -> BaseResponse:
        """
        Checks if fish is hit (according to probability distribution)
        and updates game result accordingly.
        """
        event = BetEvent.read(id=event.id)
        for reward in cls.reward_pool:
            if reward.get(reward_id) == reward_id and event:
                if _killed := cls.get_prob_distribution(reward.difficulty):
                    return cls.check_win(reward, user, event.id)
            return BaseResponse()

    @classmethod
    def check_win(cls, reward: Reward, user: User, event_id):
        """
        The check_win function is used to determine if the user has won or lost.
        The function takes in a fish object, a user object, and the bullet_id of the bullet that hit it.
        It then calculates how much money was bet on this game session by all users combined (total_bets).
        If total bets is greater than or equal to reward + rtp (the amount of money left over from previous games),
        then we can pay out our reward without going below our minimum RTP threshold for either users or the pool as a whole.
        If not, we return 0 as our winnings.

        Args:
            self: Make the method belong to the class
            objective: Get the reward value of the object
            user: Get the user's rtp and to save the game result
            event: Save the event id in the  table
            :param user:
            :param objective:
            :param event_id:
            : Check if the user has enough money to bet

        Returns:
            A  object

        """
        total_bets = (
            sum(x.betAmount for x in GameSession.userSessions) * cls.rtp_pool_max
        )

        def _save_results(_reward, _bullet_id):
            user.rtp -= _reward * cls.rtp_pool_max
            user.save()
            session = Enumerable(user.userSessions).last()
            game_result = GameResult(
                player_session_id=session.id, event_id=event_id, win=_reward
            )
            game_result.save()
            return BaseResponse(success=True, response=_reward)

        if user.rtp > cls.rtp_user_min and total_bets >= objective.reward + user.rtp:
            return _save_results(objective.reward, event_id)

    @staticmethod
    def get_probability_distribution(difficulty: int) -> int:
        """
        Returns the probability distribution for hitting a fish based on its property value.
        Assumes higher property values have lower probabilities.
        """
        seeds: float = random.random()
        difficulty_level: float = difficulty / 100
        prob_range: list = [(difficulty_level - 1) * 0.05, difficulty_level * 0.05]
        return prob_range[0] <= seeds < prob_range[1]

    @classmethod
    def reward_out(cls):
        """
        The fish_out function is a method of the Pond class. It returns a random fish object from the pond,
            and it has an equal chance of returning any type of fish in the pond. The function also has a 5% chance
            to return 3-5 small fishes instead of one large fish.

        Args:
            cls: Refer to the object itself

        Returns:
            A fish object
        """

        def _take_path():
            paths = Enumerable(cls.session.game.paths)
            taken_paths = paths.select(lambda x: not x.taken).to_list()
            path = random.choice(Paths.all())
            if path not in taken_paths:
                paths.first(lambda x: x.id == path.id).taken = True
                return path

        def _generate_reward(_reward_type: int):
            path = _take_path()
            reward_data = Reward.read(reward_type=_reward_type)
            if reward_data:
                reward_data.path = path
                yield _reward_type

        reward_type = random.randint(1, 25)
        if reward_type < 5:
            for _ in range(random.randint(3, 5)):
                return list(_generate_reward(_reward_type=reward_type))
        return list(_generate_reward(reward_type))
