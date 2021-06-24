if __name__ != '__main__':
    exit()

import matplotlib.pyplot as plt
from consts import *
from random import random

currentSpeeds: float = 0
targetSpeeds: float = 0

spds = []
ns = []
intg = [0]

cnt = 1000


for i in range(cnt):
    if i % (cnt // 30) == 0:
        targetSpeeds = random() * 2 - 1
    currentSpeeds = easeSpeed(currentSpeeds, targetSpeeds)
    spds += [currentSpeeds]
    ns += [targetSpeeds]
    intg += [intg[-1] + currentSpeeds]

plt.plot(spds, 'r')
plt.plot(ns, 'b')
plt.show()

plt.plot(intg, 'g')
plt.show()