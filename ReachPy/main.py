# imports
import sys
import inputs
from typing import Optional, List
from busio import I2C
from adafruit_pca9685 import *
from adafruit_servokit import *
from consts import *


# globals
i2c: Optional[I2C] = None
motors: Optional[ServoKit] = None
speedData: List[List[float]] = []
joystick = None


# functions
def setSpeed(pos: MotorPos, throttle: float):
    global motors, speedData
    speedData[pos.value()][2] = throttle * maxThrottle

def updateSpeed(pos: MotorPos):
    global speedData
    for i in range(len(speedData)):
        easeSpeed(speed_data=speedData[i])
        motors.continuous_servo[motorConfig[pos]].throttle = speedData[i][0]

def updateSpeeds():
    updateSpeed(MotorPos.FRONT_LEFT)
    updateSpeed(MotorPos.FRONT_RIGHT)
    updateSpeed(MotorPos.BACK_LEFT)
    updateSpeed(MotorPos.BACK_RIGHT)

# execution
class StopRun(BaseException):
    pass

def init():
    #globals
    global i2c, motors, joystick, speedData

    #initialize
    i2c = I2C(board.SCL, board.SDA)
    motors = ServoKit(channels=16, i2c=i2c)
    speedData = [list((0, 0, 0,)) for _ in range(motorCount)]


def deinit():
    pass

def run():

    isMechanum = True
    inputX, inputY = []

    iSum, iDiff = inputX + inputY, inputY - inputX

    setSpeed(MotorPos.FRONT_LEFT,  iSum if isMechanum else iDiff)
    setSpeed(MotorPos.FRONT_RIGHT, iSum)
    setSpeed(MotorPos.BACK_RIGHT,  iDiff if isMechanum else iSum)
    setSpeed(MotorPos.BACK_LEFT,   iDiff)

    updateSpeeds()


def main():
    # initialize
    init()

    # execution loop
    while True:

        try:
            # attempt to run
            run()

        except BaseException as e:
            # catch real errors and print to stderr
            if not isinstance(e, StopRun):
                sys.stderr.write(str(e))

            break

        # ensure wait between execution cycles
        time.sleep(10)

    # de-init
    deinit()

if __name__ == '__main__':
    main()