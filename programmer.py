from cv2 import add
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import numpy as np
import time
from bitarray import bitarray
from bitarray import util
from .ShiftRegister import shiftRegister

class Programmer:

    GVpp = 25
    E = 8

    dataPins = [17, 22, 9, 5, 13, 26, 12, 20, 27, 10, 11, 6, 19, 7, 16, 21]

    shiftData = 18
    shiftClock = 24
    shiftLatch = 23

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        # Setup Pins
        GPIO.setup(self.GVpp, GPIO.OUT)
        GPIO.setup(self.E, GPIO.OUT)

        for pin in self.dataPins:
            GPIO.setup(pin, GPIO.IN)

        # Setup Initial State
        GPIO.output(self.GVpp, 1)
        GPIO.output(self.E, 1)

        self.addReg = shiftRegister(self.shiftData, self.shiftClock, self.shiftLatch)

    def printOutput(self):
        data = bitarray()

        for pin in self.dataPins:
            data.append(GPIO.input(pin))
        print(util.ba2hex(data))

    def read(self, address):

        self.setAddress(address)

        GPIO.output(self.E, 0)
        GPIO.output(self.GVpp, 0)
        time.sleep(0.001)
        self.printOutput()

        GPIO.output(self.E, 1)
        GPIO.output(self.GVpp, 1)

        time.sleep(0.001)
        self.printOutput()

    def setMargin(self, set):
        if set:
            self.addReg.inputAddress('100100000000')
        else:
            self.addReg.inputAddress('10100000000')

        GPIO.output(self.E, 1)
        GPIO.output(self.GVpp, 0)
        time.sleep(0.000005)

        GPIO.output(self.GVpp, 1)
        time.sleep(0.000005)

        GPIO.output(self.E, 0)
        time.sleep(0.000005)

        if set:
            self.addReg.inputAddress('10100000000')
        else:
            self.addReg.inputAddress('100100000000')
        time.sleep(0.000005)

        GPIO.output(self.E, 1)
        time.sleep(0.000005)

        GPIO.output(self.GVpp, 0)
        time.sleep(0.000005)

        if set:
            self.addReg.inputAddress('100100000000')
        else:
            self.addReg.inputAddress('10100000000')

    def program(self, address, data):
        self.setDataPinMode(0)
        self.setData(data)
        self.setAddress(address)
        GPIO.output(self.GVpp, 1)
        GPIO.output(self.E, 1)
        time.sleep(0.000005)

        GPIO.output(self.E, 0)
        time.sleep(0.00005)
        GPIO.output(self.E, 1)
        time.sleep(0.000005)

        GPIO.output(self.GVpp, 0)
        self.setDataPinMode(1)
        time.sleep(0.000005)

        GPIO.output(self.E, 0)
        time.sleep(0.000005)

        self.printOutput()
        time.sleep(0.000005)

        self.setDataPinMode(0)
        GPIO.output(self.E, 1)
        time.sleep(0.000005)



    def setAddress(self, address):
        addr = util.int2ba(address)
        self.addReg.inputAddress(addr)

    def setData(self, data):
        data = util.hex2ba(data)
        for i, bit in enumerate(data):
            GPIO.output(self.dataPins[i], int(bit))
            print(bit)

    def setDataPinMode(self, mode):
        modeSet = GPIO.IN if mode == 1 else GPIO.OUT
        for pin in self.dataPins:
            GPIO.setup(pin, modeSet)


def main():
    prog = Programmer()

    prog.read(0)
    GPIO.cleanup()


if __name__ == "__main__":
    main()