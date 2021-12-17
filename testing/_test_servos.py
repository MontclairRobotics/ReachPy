from adafruit_servokit import *
import time

kit = ServoKit(channels=16)
kit.frequency = 100
kit.continuous_servo[0].set_pulse_width_range(1000,2000)
#kit.continuous_servo[1].set_pulse_width_range(1000,2000)
kit.continuous_servo[2].set_pulse_width_range(1000,2000)
kit.continuous_servo[3].set_pulse_width_range(1000,2000)

#kit.continuous_servo[0].throttle = 0.1
#time.sleep(2)
kit.continuous_servo[0].throttle = .15
#kit.continuous_servo[1].throttle = .15
kit.continuous_servo[2].throttle = .15
kit.continuous_servo[3].throttle = .15