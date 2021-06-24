if __name__ != '__main__':
    exit()

from evdev import *

print(ecodes.EV)

devNum = 4
devP = '/dev/input/event' + str(devNum)
dev = InputDevice(devP)

btn_1 = 288
btn_2 = 290
btn_3 = 289

x_ax = 0
y_ax = 1

while True:
    tmp = dev.absinfo(1)
    if tmp:
        print(type(tmp))
        print(tmp)