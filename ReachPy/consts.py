import math
from enum import IntEnum, unique
from typing import Dict, Tuple, List

maxThrottle: float = 0.1
"""The maximum throttle for the motor"""

motorCount: int = 4
"""The number of motors"""

@unique
class MotorPos(IntEnum):
    FRONT_LEFT = 1
    FRONT_RIGHT = 2
    BACK_LEFT = 3
    BACK_RIGHT = 4

motorConfig: Dict[MotorPos, int] = {
    MotorPos.FRONT_RIGHT: 1,
    MotorPos.FRONT_LEFT: 2,
    MotorPos.BACK_RIGHT: 3,
    MotorPos.BACK_LEFT: 4
}
"""The motor configuration"""

def clamp(val: float, min_val: float, max_val: float) -> float:
    """Clamp a float value to a given range"""
    return min(max(val, min_val), max_val)

def clampMag(val: float, min_val: float, max_val: float) -> float:
    """Clamp a float value's magnitude to a given range"""
    n = clamp(abs(val), min_val, max_val)
    return math.copysign(1, val) * n

speedPreservationFactor: float = 15
"""A factor which controls how much the speeds are preserved after
   a call to ease"""

def easeSpeed(current_speed: float, target_speed: float) -> float:
    """Ease the speed using an acceleration factor"""
    return current_speed + (target_speed - current_speed) / (speedPreservationFactor + 1)

devicePath = 'dev/input/event4'
"""Device path for input"""