from enum import Enum, unique

maxThrottle: float = 0.1
"""The maximum throttle for the motor"""

@unique
class MotorPos(Enum):
    FRONT_LEFT = 1
    FRONT_RIGHT = 2
    BACK_LEFT = 3
    BACK_RIGHT = 4

motorConfig: dict = {
    MotorPos.FRONT_RIGHT: 1,
    MotorPos.FRONT_LEFT: 2,
    MotorPos.BACK_RIGHT: 3,
    MotorPos.BACK_LEFT: 4
}
"""The motor configuration"""