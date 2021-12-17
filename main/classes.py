import time

#########################################################
##                       Classes                       ##
#########################################################

class ToggleStateMonitor:
    """A class which keeps track of a toggleable state."""

    def __init__(self, start_value: bool):
        self._previous = False
        self._current = False
        self.value = start_value

    def update(self, value: bool) -> None:
        self._previous = self._current
        self._current = value

        if self._current and not self._previous:
            self.value = not self.value

class TimeMonitor:
    """A class which keeps track of changes in time."""

    def __init__(self):
        self._previous = time.time_ns()
        self._current  = time.time_ns()

    def update(self):
        self._previous = self._current
        self._current = time.time_ns()

    def delta_ns(self) -> int:
        return self._current - self._previous
    def delta_secs(self) -> float:
        return self.delta_ns() / 1_000_000_000