# utils.py
from collections import deque

# Moving Average Class
# Calculate moving average of stream of numbers based on a window size
# param window_size: int
# return: float
class MovingAverage:
    def __init__(self, window_size=10):
        self.window = deque(maxlen=window_size)

    def update(self, new_val):
        self.window.append(new_val)
        return sum(self.window) / len(self.window) if self.window else new_val
