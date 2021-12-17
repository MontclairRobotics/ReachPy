from enum import IntEnum, unique

#########################################
##              Constants              ##
#########################################

"""The maximum throttle allowed in fast mode"""
max_throttle_fast: float = 0.25
"""The maximum throttle allowed in non-fast mode"""
max_throttle_slow: float = 0.15

"""The number of motors"""
motor_count: int = 4

@unique
class MotorPos(IntEnum):
    """Motor positions"""
    FRONT_LEFT = 0
    FRONT_RIGHT = 1
    BACK_LEFT = 2
    BACK_RIGHT = 3

"""All of the motor positions"""
all_motor_pos: set[MotorPos] = {
    MotorPos.FRONT_RIGHT,
    MotorPos.FRONT_LEFT,
    MotorPos.BACK_LEFT,
    MotorPos.BACK_RIGHT
}

"""The motor configuration"""
motor_config: dict[MotorPos, int] = {
    MotorPos.FRONT_RIGHT: 0,
    MotorPos.FRONT_LEFT: 1,
    MotorPos.BACK_RIGHT: 2,
    MotorPos.BACK_LEFT: 3
}

"""The factors which all motor speeds will be multiplied by (due to orientation)"""
motor_factors: dict[MotorPos, float] = {
    MotorPos.FRONT_LEFT: -1,
    MotorPos.FRONT_RIGHT: 1,
    MotorPos.BACK_LEFT:   1,
    MotorPos.BACK_RIGHT: -1
}

sec_to_ease_one_unit: float = 0.5
"""A factor which controls how much the speeds are preserved after
   a call to ease"""

"""The id of the mechanum button toggle."""
btn_mchn = 288
"""The id of the stop button toggle."""
btn_stop = 290
"""The id of the fast button toggle."""
btn_fast = 289

"""The x-axis id"""
x_axis = 0
"""The y-axis id"""
y_axis = 1
