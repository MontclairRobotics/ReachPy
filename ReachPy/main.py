# imports
import sys
import evdev
from evdev import InputDevice
from typing import Optional, List
from adafruit_pca9685 import *
from adafruit_servokit import *
from consts import *


# globals
motors: Optional[ServoKit] = None

currentSpeeds: List[float] = []
targetSpeeds: List[float] = []

controller: Optional[InputDevice] = None

isFast: bool = False
isMchn: bool = False
isStop: bool = False

prsFast: bool = False
prsMchn: bool = False
prsStop: bool = False

prevFast: bool = False
prevMchn: bool = False
prevStop: bool = False

# functions
def resetSpeeds():
    global currentSpeeds, targetSpeeds
    currentSpeeds = [0] * motorCount
    targetSpeeds = [0] * motorCount

def setSpeed(pos: MotorPos, throttle: float, slow: bool):
    targetSpeeds[pos.value] = throttle * maxThrottle(slow)

def updateSpeed(pos: MotorPos):
    global currentSpeeds, targetSpeeds
    currentSpeeds[pos.value] = easeSpeed(currentSpeeds[pos.value], targetSpeeds[pos.value])
    
    mul = -1
    if pos == MotorPos.FRONT_LEFT or pos == MotorPos.BACK_LEFT:
        mul = 1
    
    motors.continuous_servo[motorConfig[pos]].throttle = fixServoOuchie(mul * currentSpeeds[pos.value])

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
    global motors, controller

    #initialize
    motors = ServoKit(channels=16)

    resetSpeeds()

    controller = InputDevice(devicePath)
    controller.grab()

def deinit():
    global controller, motors
    controller.ungrab()
    controller.close()

def handleInputs():
    global isMchn, isFast, isStop, prsMchn, prsFast, prsStop, prevMchn, prevFast, prevStop

    active_buttons = controller.active_keys()

    prevMchn = prsMchn
    prevStop = prsStop
    prevFast = prsFast

    prsMchn = btn_1 in active_buttons
    prsStop = btn_2 in active_buttons
    prsFast = btn_3 in active_buttons

    if not prevStop and prsStop:
        isStop = not isStop

    if not prevMchn and prsMchn:
        isMchn = not isMchn

    if not prevFast and prsFast:
        isFast = not isFast

def run():
    handleInputs()

    if isStop:
        resetSpeeds()
        
    else:
        inputX = getAbsVal(controller.absinfo(x_ax))
        inputY = getAbsVal(controller.absinfo(y_ax))

        iSum, iDiff = inputX + inputY, inputY - inputX

        if isMchn and abs(inputY) <= 0.5:
            iSum *= abs(inputX) * 4 + 1
            iDiff *= abs(inputX) * 4 + 1
            iSum = clamp(iSum, -1, 1)
            iDiff = clamp(iDiff, -1, 1)

        setSpeed(MotorPos.FRONT_LEFT, iSum if isMchn else iDiff, isFast)
        setSpeed(MotorPos.FRONT_RIGHT, iSum, isFast)
        setSpeed(MotorPos.BACK_RIGHT,  iDiff if isMchn else iSum, isFast)
        setSpeed(MotorPos.BACK_LEFT,   iDiff, isFast)

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
                print(e)

            break

        # ensure wait between execution cycles
        time.sleep(0.02)

    # de-init
    deinit()

if __name__ == '__main__':
    main()
