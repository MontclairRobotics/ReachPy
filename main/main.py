#! /usr/bin/python3
# used for startup

import sys
import time
import evdev
from evdev import InputDevice, list_devices
from typing import List
from adafruit_pca9685 import *
from adafruit_servokit import *

from classes import *
from utils import *

#######################################
##              Program              ##
#######################################

def setup_controller() -> InputDevice:
    """Setup the controller."""

    devices: List[InputDevice] = [InputDevice(path) for path in list_devices()]

    def device_predicate(dev: InputDevice) -> bool:
        return 'DragonRise Inc.' in dev.name and 'Joystick' in dev.name

    possible_controllers = list(filter(device_predicate, devices))
    if len(possible_controllers) != 1:
        raise IOError('Controller not found.')

    debug('controller.path = ' + possible_controllers[0].path)
    debug('controller.capabilities = ' + str(possible_controllers[0].capabilities()))

    controller = possible_controllers[0]
    return controller

class Program:

    def __init__(self):

        self.motors = ServoKit(channels=16)

        self.controller = setup_controller()
        self.controller.grab()

        self.isFast = ToggleStateMonitor(False)
        self.isMchn = ToggleStateMonitor(False)
        self.isStop = ToggleStateMonitor(True)

        self.currentSpeeds = {k : 0 for k in all_motor_pos}
        self.targetSpeeds  = {k : 0 for k in all_motor_pos}

        self.timeMonitor = TimeMonitor()

    def set_speed(self, pos, throttle, is_fast):
        self.targetSpeeds[pos] = throttle * max_throttle(is_fast)

    def update_speeds(self):
        for pos in all_motor_pos:
            self.currentSpeeds[pos] = ease_speed(self.currentSpeeds[pos], self.targetSpeeds[pos], self.timeMonitor.delta_secs())

            spd = self.currentSpeeds[pos]
            spd *= motor_factors[pos]
            spd = adjust_speed_for_motors(spd)

            self.set_motor_throttle(pos, spd)

    def set_motor_throttle(self, pos, val):
        self.motors.continuous_servo[motor_config[pos]].throttle = val

    def stop_all(self):
        for pos in all_motor_pos:
            self.currentSpeeds[pos] = 0
            self.targetSpeeds[pos]  = 0

    def handle_inputs(self):
        active_buttons = self.controller.active_keys()

        self.isMchn.update(btn_mchn in active_buttons)
        self.isStop.update(btn_stop in active_buttons)
        self.isFast.update(btn_fast in active_buttons)

    def run(self):
        while True:
            self.timeMonitor.update()
            self.handle_inputs()

            if self.isStop.value:
                self.stop_all()
            else:
                inputX = remap_abs_info(self.controller.absinfo(x_axis))
                inputY = remap_abs_info(self.controller.absinfo(y_axis))

                inputSum, inputDiff = inputX + inputY, inputX - inputY

                # Code to adjust for mechanum; not needed but interesting :)

                # if isMchn and abs(inputY) <= 0.5:
                #     inputSum *= abs(inputX) * 6 + 1
                #     inputDiff *= abs(inputX) * 6 + 1
                #     inputSum = clamp(inputSum, -1, 1)
                #     inputDiff = clamp(inputDiff, -1, 1)

                isFast = self.isFast.value
                isMchn = self.isMchn.value

                self.set_speed(MotorPos.FRONT_LEFT,  inputDiff,                         isFast)
                self.set_speed(MotorPos.FRONT_RIGHT, inputSum,                          isFast)
                self.set_speed(MotorPos.BACK_LEFT,   inputSum if isMchn else inputDiff, isFast)
                self.set_speed(MotorPos.BACK_RIGHT,  inputDiff if isMchn else inputSum, isFast)

            self.update_speeds()

    def __del__(self):
        self.controller.ungrab()
        self.controller.close()


#####################################
##          Main function          ##
#####################################
def main():
    prog = None

    try:
        prog = Program()
        prog.run()
    except Exception:
        del prog
        raise


###################################
##        Main entrypoint        ##
###################################
if __name__ == '__main__':
    main()
