from typing import final

import time

from ._utils import metadata

from ._utils.common import to_milliseconds, to_seconds, Singleton

__all__ = [
    'get_ticks',
    'wait',
    'delay',
    'set_timer',
    'Clock'
]

def get_ticks():
    return to_milliseconds(time.monotonic() - metadata.LOAD_TIME)

def wait(milliseconds):
    time.sleep(to_seconds(milliseconds))

def delay(milliseconds):
    time.sleep(to_seconds(milliseconds))

def set_timer(event, millis, loops=0):
    pass

# source from: https://pypi.org/project/pygclock
@final
class Clock(Singleton):
    _last_tick = 0.0
    _time_elapsed = 0.0
    _fps = 0.0
    _raw_time = 0.0

    def tick(self, framerate):
        current_time = time.monotonic()
        elapsed_time = current_time - self._last_tick

        if framerate > 0:
            min_frame_time = 1 / framerate
            if elapsed_time < min_frame_time:
                time.sleep(min_frame_time - elapsed_time)

        current_time = time.monotonic()

        self._fps = 1 / (current_time - self._last_tick) if current_time != self._last_tick else 0.0
        self._time_elapsed = current_time - self._last_tick
        self._raw_time = elapsed_time
        self._last_tick = current_time

        return to_milliseconds(self._time_elapsed)

    def get_time(self):
        return to_milliseconds(self._time_elapsed)

    def get_rawtime(self):
        return to_milliseconds(self._raw_time)

    def get_fps(self):
        return self._fps