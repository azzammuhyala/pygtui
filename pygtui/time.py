import time

from .utils.error import check_initialized
from .utils import metadata

def get_ticks():
    check_initialized()
    return time.time() - metadata.TIME_INITIALIZE

def wait(n):
    time.sleep(n)

# code from: https://pypi.org/project/pygclock
class Clock:

    def __init__(self):
        self._last_tick = time.time()
        self._time_elapsed = 0.0
        self._fps = 0.0
        self._raw_time = 0.0

    def tick(self, framerate) -> float:
        current_time = time.time()
        elapsed_time = current_time - self._last_tick

        if framerate > 0:
            min_frame_time = 1 / framerate
            if elapsed_time < min_frame_time:
                time.sleep(min_frame_time - elapsed_time)

        current_time = time.time()

        self._fps = 1 / (current_time - self._last_tick) if current_time != self._last_tick else 0.0
        self._time_elapsed = current_time - self._last_tick
        self._raw_time = elapsed_time
        self._last_tick = current_time

        return self._time_elapsed

    def get_time(self) -> float:
        return self._time_elapsed

    def get_rawtime(self) -> float:
        return self._raw_time

    def get_fps(self) -> float:
        return self._fps