"""
@author: Kuro
"""
from datetime import datetime


class Timer:
    def __init__(self):
        pass

    def start(self):
        self.time_start = datetime.now()
        return

    def end(self):
        end = datetime.now()
        print("Execution time: ", abs(self.time_start - end))
