# imports
import sys
import evdev
from typing import Optional, List
from adafruit_pca9685 import *
from adafruit_servokit import *
from consts import *


# globals
motors: Optional[ServoKit] = None

currentSpeeds: List[float] = []
targetSpeeds: List[float] = []

controller = None


# functions
def setSpeed(pos: MotorPos, throttle: float):
    targetSpeeds[pos.value] = throttle * maxThrottle

def updateSpeed(pos: MotorPos):
    global currentSpeeds, targetSpeeds
    for i in range(motorCount):
        currentSpeeds[i] = easeSpeed(currentSpeeds[i], targetSpeeds[i])
        motors.continuous_servo[motorConfig[pos]].throttle = currentSpeeds[i]

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
    global motors, currentSpeeds, targetSpeeds, controller

    #initialize
    motors = ServoKit(channels=16)

    currentSpeeds = list((0,) * motorCount)
    targetSpeeds  = list((0,) * motorCount)

    #controller = InputDevice(devicePath)


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