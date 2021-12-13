# imports
import sys
import evdev
from evdev import InputDevice, list_devices
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
isStop: bool = True

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

def setup_controller():
    global controller
    
    devices: List[InputDevice] = [InputDevice(path) for path in list_devices()]
    
    def device_predicate(dev: InputDevice) -> bool:
        return 'DragonRise Inc.' in dev.name and 'Joystick' in dev.name
    
    possible_controllers = list(filter(device_predicate, devices))
    if len(possible_controllers) != 1:
        debug('Controller not found')
        sys.exit(1)
    
    debug('controller.path = ' + possible_controllers[0].path)
    debug('controller.capabilities = ' + str(possible_controllers[0].capabilities()))
    
    controller = possible_controllers[0]
    controller.grab()

def init():
    #globals
    global motors

    #initialize
    motors = ServoKit(channels=16)

    resetSpeeds()
    setup_controller()

def deinit():
    global controller, motors

    resetSpeeds()
    updateSpeeds()

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

        inputSum, inputDiff = inputX + inputY, inputY - inputX

        # if isMchn and abs(inputY) <= 0.5:
        #     inputSum *= abs(inputX) * 6 + 1
        #     inputDiff *= abs(inputX) * 6 + 1
        #     inputSum = clamp(inputSum, -1, 1)
        #     inputDiff = clamp(inputDiff, -1, 1)

        setSpeed(MotorPos.FRONT_LEFT, inputDiff, isFast)
        setSpeed(MotorPos.FRONT_RIGHT, inputSum, isFast)
        setSpeed(MotorPos.BACK_LEFT, inputSum if isMchn else inputDiff, isFast)
        setSpeed(MotorPos.BACK_RIGHT, inputDiff if isMchn else inputSum, isFast)
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
