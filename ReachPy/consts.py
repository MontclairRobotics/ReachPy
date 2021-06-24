import math
from evdev import AbsInfo
from enum import IntEnum, unique
from typing import Dict, Tuple, List

def maxThrottle(slow: bool) -> float:
    if slow:
        return 0.09
    else:
        return 0.18
"""The maximum throttle for the motor"""

motorCount: int = 4
"""The number of motors"""

@unique
class MotorPos(IntEnum):
    """Motor positions"""
    FRONT_LEFT = 0
    FRONT_RIGHT = 1
    BACK_LEFT = 2
    BACK_RIGHT = 3

motorConfig: Dict[MotorPos, int] = {
    MotorPos.FRONT_RIGHT: 0,
    MotorPos.FRONT_LEFT: 1,
    MotorPos.BACK_RIGHT: 2,
    MotorPos.BACK_LEFT: 3
}
"""The motor configuration"""

def clamp(val: float, min_val: float, max_val: float) -> float:
    """Clamp a float value to a given range"""
    return min(max(val, min_val), max_val)

def clampMag(val: float, min_val: float, max_val: float) -> float:
    """Clamp a float value's magnitude to a given range"""
    n = clamp(abs(val), min_val, max_val)
    return math.copysign(1, val) * n

speedPreservationFactor: float = 3
"""A factor which controls how much the speeds are preserved after
   a call to ease"""

def easeSpeed(current_speed: float, target_speed: float) -> float:
    """Ease the speed using an acceleration factor"""
    return current_speed + (target_speed - current_speed) / (speedPreservationFactor + 1)

devicePath = '/dev/input/event0'
"""Device path for input"""

btn_1 = 288
"""The id of the first button"""
btn_2 = 290
"""The id of the second button"""
btn_3 = 289
"""The id of the thirst button"""

x_ax = 0
"""The x-axis id"""
y_ax = 1
"""The y-axis id"""

def remap(val: float, basemin: float, basemax: float, newmin: float, newmax: float) -> float:
    """Take a float value and re-map it into a new range given its expected range"""
    return ((val - basemin) / (basemax - basemin)) * (newmax - newmin) + newmin

def getAbsVal(absv: AbsInfo) -> float:
    """Do the thing"""
    return remap(absv.value, absv.min, absv.max, -1, 1)

def fixServoOuchie(spd: float) -> float:
    """i hate everythinggggggg"""
    return spd + 0.125
