import math
from enum import IntEnum, unique
from typing import TypedDict, Tuple, List

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

motorConfig: TypedDict[MotorPos, int] = \
{
    MotorPos.FRONT_RIGHT: 1,
    MotorPos.FRONT_LEFT: 2,
    MotorPos.BACK_RIGHT: 3,
    MotorPos.BACK_LEFT: 4
}
"""The motor configuration"""

def maxMag(val: float, max_val: float) -> float:
    return math.copysign(val, max(abs(val), max_val))
"""Clamp a float value's magnitude to a given range"""

easeForceAdd: float = 0.005
"""How much will the ease function be guaranteed to change by"""
speedPow: float = 4
"""A factor which controls how much the speeds are preserved after
   a call to ease"""
baseSpeedMul: float = 3
"""A factor which controls how much the speeds are preserved after
   a call to ease"""

def easeSpeed(speed_data: List[float]):

    base = speed_data[0]
    base_ds = speed_data[1]
    target = speed_data[2]

    if abs(base - target) < easeForceAdd:
        speed_data[0] = target
        speed_data[1] = 0
        return

    new_val = base
    target_speed = target - base

    new_ds = ((baseSpeedMul * base_ds ** speedPow + target_speed ** speedPow) / (baseSpeedMul + 1)) ** \
             (1 / speedPow)
    new_ds = maxMag(new_ds, target_speed)

    new_val += new_ds
    new_val = maxMag(new_val, target)

    if new_val == target:
        speed_data[0] = target
        speed_data[1] = 0
    else:
        speed_data[0] = new_val
        speed_data[1] = new_ds
