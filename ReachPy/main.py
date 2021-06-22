# imports
import sys
import inputs
from typing import Optional
from busio import I2C
from adafruit_pca9685 import *
from adafruit_servokit import *
from consts import *


# globals
i2c: Optional[I2C] = None
motors: Optional[ServoKit] = None
joystick = None


# functions
def setSpeed(pos: MotorPos, throttle: float):
    motors.continuous_servo[motorConfig[pos]].throttle = throttle * maxThrottle


# execution
class StopRun(BaseException):
    pass

def init():
    #globals
    global i2c, motors, joystick

    #initialize
    i2c = I2C(board.SCL, board.SDA)
    motors = ServoKit(channels=16, i2c=i2c)


def deinit():
    pass

def run():

    isMechanum = True
    inputX, inputY = []

    iSum, iDiff = inputX + inputY, inputY - inputX

    setSpeed(MotorPos.FRONT_LEFT, iSum if isMechanum else iDiff)
    setSpeed(MotorPos.FRONT_RIGHT, iSum)
    setSpeed(MotorPos.BACK_RIGHT, iDiff if isMechanum else iSum)
    setSpeed(MotorPos.BACK_LEFT, iDiff)


def main():
    # initialize
    init()

    # execution loop
    while True:

        try:
            # attempt to run
            run()

        except object as e:
            # catch real errors and print to stderr
            if not isinstance(e, StopRun):
                sys.stderr.write(str(e))

            break

        # ensure wait between execution cycles
        time.sleep(10)

    # deinit
    deinit()

if __name__ == '__main__':
    main()