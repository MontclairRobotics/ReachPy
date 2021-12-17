import math
from evdev import AbsInfo
from consts import *

###################################
##       Utility functions       ##
###################################

def ease_speed(current_speed: float, target_speed: float, delta_sec: float) -> float:
    """Ease between the current value and target value with a constant slope defined
       by sec_to_ease_one_unit."""
    target_delta = delta_sec / sec_to_ease_one_unit

    delta = target_speed - current_speed
    delta_clamp = clamp(delta, -target_delta, target_delta)

    if abs(delta) < abs(delta_clamp):
        return target_speed

    return current_speed + delta_clamp

def remap(val: float, basemin: float, basemax: float, newmin: float, newmax: float) -> float:
    """Take a float value and re-map it into a new range given its expected range"""
    return ((val - basemin) / (basemax - basemin)) * (newmax - newmin) + newmin

def remap_abs_info(absv: AbsInfo) -> float:
    """Do the thing"""
    return remap(absv.value, absv.min, absv.max, -1, 1)

def adjust_speed_for_motors(spd: float) -> float:
    """Adjust the speed value to be aligned with errors in motors."""
    return clamp(spd + 0.125, -1, 1)

def clamp(val: float, min_val: float, max_val: float) -> float:
    """Clamp a float value to a given range"""
    return min(max(val, min_val), max_val)

def clamp_mag(val: float, min_val: float, max_val: float) -> float:
    """Clamp a float value's magnitude to a given range"""
    n = clamp(abs(val), min_val, max_val)
    return math.copysign(1, val) * n

def debug(msg: str):
    """Print a debug message."""
    print("DEBUG MESSAGE: " + msg)

def max_throttle(fast: bool) -> float:
    """The maximum throttle for the motor"""
    return max_throttle_fast if fast else max_throttle_slow