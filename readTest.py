import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import numpy as np
import time
from bitarray import bitarray
from bitarray import util

class shiftRegister:
    def __init__(self, data, serialClock, registerClock):
        self.ser = data
        self.srlclck = serialClock
        self.rclk = registerClock

        GPIO.setup(self.ser, GPIO.OUT)
        GPIO.setup(self.srlclck, GPIO.OUT)
        GPIO.setup(self.rclk, GPIO.OUT)

        self.setup()

    def setup(self):
        GPIO.output(self.ser, 0)
        GPIO.output(self.srlclck, 0)
        GPIO.output(self.rclk, 0)

        self.clear()

    def clear(self):
        GPIO.output(self.ser, 0)
        for i in range(0, 24):
            self.shift()
        
        self.latch()

    def shift(self):
        GPIO.output(self.srlclck, 0)
        GPIO.output(self.srlclck, 1)
        GPIO.output(self.srlclck, 0)

    def latch(self):
        GPIO.output(self.rclk, 0)
        GPIO.output(self.rclk, 1)
        GPIO.output(self.rclk, 0)

    def inputBit(self, value):
        GPIO.output(self.ser, value)
        self.shift()

    def inputAddress(self, bitArray):
        for bit in bitArray:
            self.inputBit(bit)
        self.latch()


class Programmer:

    GVpp = 25
    E = 8
    dataPins = [17, 22, 9, 5, 21, 16, 7, 19, 27, 10, 11, 6, 20, 12, 26, 13]

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


    def shift_address(self, data):
        self.address_register = data + self.address_register
        self.address_register = self.address_register[0:21]

    def read(self):

        data = bitarray()

        for pin in self.dataPins:
            data.append(GPIO.input(pin))
        print(util.ba2hex(data))

        GPIO.output(self.E, 0)
        GPIO.output(self.GVpp, 0)
        time.sleep(0.001)

        data = bitarray()

        for pin in self.dataPins:
            data.append(GPIO.input(pin))
        print(util.ba2hex(data))

        GPIO.output(self.E, 1)
        GPIO.output(self.GVpp, 1)

        time.sleep(0.001)

        data = bitarray()
        
        for pin in self.dataPins:
            data.append(GPIO.input(pin))
        print(util.ba2hex(data))

    def setAddress(self):
        data = bitarray('1010')
        self.addReg.inputAddress(data)

        data = bitarray()
        
        for pin in self.dataPins:
            data.append(GPIO.input(pin))
        print(data)


def main():
    prog = Programmer()

    prog.read()
    GPIO.cleanup()


if __name__ == "__main__":
    main()