import sys
import inputs
from busio import I2C
from adafruit_pca9685 import *
from adafruit_servokit import *

i2c = None
servos = None


class StopRun(BaseException):
    pass

def init():
    #globals
    global i2c, servos

    #initialize
    i2c = I2C(board.SCL, board.SDA)
    servos = ServoKit(channels=16, i2c=i2c)


def deinit():
    pass

def run():
    pass




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