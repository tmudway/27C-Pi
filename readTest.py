#import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import numpy as np

class Programmer:

    GVpp = 25
    E = 8

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

    # Setup Initial State
    GPIO.output(GVpp, 1)
    GPIO.output(E, 1)

    def log_margin(self, time):
        for i in range(time):
            self.GvppLog.append(self.GVpp)
            self.ELog.append(self.E)
            self.A8Log.append(self.address_register[8])
            self.A10Log.append(self.address_register[10])

    def view_log_margin(self):
        plt.plot(np.array(self.A8Log) + 6)
        plt.plot(np.array(self.GvppLog) + 4)
        plt.plot(np.array(self.ELog) + 2)
        plt.plot(self.A10Log)
        plt.legend(["A8", "GVpp", "E", "A10"])
        plt.show()

    def shift_address(self, data):
        self.address_register = data + self.address_register
        self.address_register = self.address_register[0:21]

    def set_margin(self, setOrReset):

        # Initial State
        self.shift_address([0,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0])
        self.GVpp = 0
        self.E = 1
        self.log_margin(5)

        self.GVpp = 1
        self.log_margin(5)

        self.E = 0
        self.log_margin(5)

        self.shift_address([0])
        self.log_margin(5)

        self.E = 1
        self.log_margin(5)

        self.GVpp = 0
        self.log_margin(5)
        
        self.shift_address([0,0,0])
        self.log_margin(5)

    def program(self, data):
        pass

def main():
    prog = Programmer()

    prog.set_margin(1)
    prog.view_log_margin()
    GPIO.cleanup()


if __name__ == "__main__":
    main()