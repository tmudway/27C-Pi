import RPi.GPIO as GPIO
import time
from bitarray import bitarray
from bitarray import util
from ShiftRegister import shiftRegister

class Programmer:

    GVpp = 8
    E = 25

    dataPins = [17, 22, 9, 5, 13, 26, 12, 20, 27, 10, 11, 6, 19, 7, 16, 21]

    shiftData = 18
    shiftClock = 24
    shiftLatch = 23

    sleepWait = 0.000002

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        # Setup Pins
        GPIO.setup(self.GVpp, GPIO.OUT)
        GPIO.setup(self.E, GPIO.OUT)

        for pin in self.dataPins:
            GPIO.setup(pin, GPIO.IN)

        # Setup Initial State
        GPIO.output(self.GVpp, 0)
        GPIO.output(self.E, 0)

        self.addReg = shiftRegister(self.shiftData, self.shiftClock, self.shiftLatch)

    def getOutput(self, output = 0):
        data = bitarray()

        for pin in self.dataPins:
            data.append(GPIO.input(pin))
        dataHex = util.ba2hex(data)
        if output:
            print(dataHex[0:2], end=' ')
            print(dataHex[2:], end=' ')

        return data

    def checkBlank(self):
        self.setDataPinMode(1)
        GPIO.output(self.E, 0)
        GPIO.output(self.GVpp, 0)

        writeCount = 0

        for i in range(0, 2000000):
            data = self.readWord(i)
            if data != util.hex2ba("FFFF"):
                writeCount += 1

        if writeCount == 0:
            print("\nBlank EPROM!")
        else:
            print("\nWARNING: EPROM not blank, {0} non-blank words found".format(writeCount))


    def read(self, start = 0, end = 2000000):
        self.setDataPinMode(1)
        GPIO.output(self.E, 0)
        GPIO.output(self.GVpp, 0)

        for i in range(start, end):
            self.readWord(i)

    def readWord(self, address):
        self.setAddress(address)
        data = self.getOutput(1)
        return data

    def program(self, data, start = 0):
        self.setMargin(1)
        GPIO.output(self.E, 1)
        self.setDataPinMode(0)

        for i in range(start, start + len(data)):
            self.programWord(i, data[i - start])

        self.setMargin(0)

    def setMargin(self, set):
        if set:
            self.addReg.inputAddress('00100000000')
        else:
            self.addReg.inputAddress('10100000000')

        GPIO.output(self.E, 1)
        GPIO.output(self.GVpp, 0)
        time.sleep(self.sleepWait)

        GPIO.output(self.GVpp, 1)
        time.sleep(self.sleepWait)

        GPIO.output(self.E, 0)
        time.sleep(self.sleepWait)

        if set:
            self.addReg.inputAddress('10100000000')
        else:
            self.addReg.inputAddress('00100000000')
        time.sleep(self.sleepWait)

        GPIO.output(self.E, 1)
        time.sleep(self.sleepWait)

        GPIO.output(self.GVpp, 0)
        time.sleep(self.sleepWait)

        if set:
            self.addReg.inputAddress('00100000000')
        else:
            self.addReg.inputAddress('10100000000')

    def programWord(self, address, data):

        badRead = True
        count = 0

        while badRead:

            self.setData(data)
            self.setAddress(address)
            GPIO.output(self.GVpp, 1)
            time.sleep(self.sleepWait)

            GPIO.output(self.E, 0)
            time.sleep(0.00005)
            GPIO.output(self.E, 1)
            time.sleep(self.sleepWait)

            GPIO.output(self.GVpp, 0)
            self.setDataPinMode(1)
            time.sleep(self.sleepWait)

            GPIO.output(self.E, 0)
            time.sleep(self.sleepWait)

            readDat = self.getOutput(0)
            if readDat == util.hex2ba(data):
                badRead = False
                print("PASS - ADDRESS: {0} DATA: {1}".format(address, data))
            else:
                count += 1

            self.setDataPinMode(0)
            GPIO.output(self.E, 1)
            time.sleep(self.sleepWait)

            if count > 25:
                print("FAIL - ADDRESS: {0} DATA: {1}".format(address, data))
                #exit()
                break

    def setAddress(self, address):
        addr = util.int2ba(address+2**23)
        self.addReg.inputAddress(addr)

    def setData(self, data):
        data = util.hex2ba(data)
        for i, bit in enumerate(data):
            GPIO.output(self.dataPins[i], int(bit))

    def setDataPinMode(self, mode):
        modeSet = GPIO.IN if mode == 1 else GPIO.OUT
        for pin in self.dataPins:
            GPIO.setup(pin, modeSet)

prog = Programmer()

def main():
    start = time.perf_counter()

    iStart = 0
    iCount = 2000000

    data = ["F0F0"] * (iCount - iStart)

    #prog.program(data, iStart)
    #prog.read(iStart, iCount)
    prog.checkBlank()
        
    print(time.perf_counter() - start)
    
    GPIO.cleanup()
    print("")


if __name__ == "__main__":
    main()
