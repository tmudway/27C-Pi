import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import numpy as np
import time

class Programmer:

    GVpp = 25
    E = 8
    data = [17, 22, 9, 5, 21, 16, 7, 19, 27, 10, 11, 6, 20, 12, 26, 13]

    shift_data = 2
    shift_clock = 3
    shift_latch = 4

    address_register = []

    GvppLog = []
    ELog = []
    A8Log = []
    A10Log = []

    GPIO.setmode(GPIO.BCM)

    # Setup Pins
    GPIO.setup(GVpp, GPIO.OUT)
    GPIO.setup(E, GPIO.OUT)

    for pin in data:
        GPIO.setup(pin, GPIO.IN)

    # Setup Initial State
    GPIO.output(GVpp, 1)
    GPIO.output(E, 1)

    def shift_address(self, data):
        self.address_register = data + self.address_register
        self.address_register = self.address_register[0:21]

    def read(self):
        GPIO.output(self.E, 0)
        GPIO.output(self.GVpp, 0)
        time.sleep(0.001)

        for pin in self.data:
            print(GPIO.input(pin))


def main():
    prog = Programmer()

    prog.read()
    GPIO.cleanup()


if __name__ == "__main__":
    main()