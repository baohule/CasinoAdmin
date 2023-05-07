"""
@author: igor
"""
from app import logging
from typing import List, Union, Iterator

from app.rpc.history.schema import BetHistory
from app.rpc.history.schema import ActionHistory


logger = logging.getLogger("history")
logger.addHandler(logging.StreamHandler())


def insert_bet_history(content:BetHistory):
    """
    """
def insert_action_history(content:ActionHistory):
    """
    """