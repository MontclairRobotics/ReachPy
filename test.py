from evdev import *

print(ecodes.EV)

devNum = 4
devP = '/dev/input/event' + str(devNum)
dev = InputDevice(devP)

for event in dev.read_loop():
    if event.type == ecodes.EV_SYN:
        continue
    print(str(event) + ' ::: ' + str(categorize(event)))