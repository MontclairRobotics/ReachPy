#########################################################
##                       Classes                       ##
#########################################################

class ToggleStateMonitor:

    def __init__(self, start_value: bool):
        self._previous = False
        self._current = False
        self.value = start_value

    def update(self, value: bool) -> None:
        self._previous = self._current
        self._current = value

        if self._current and not self._previous:
            self.value = not self.value