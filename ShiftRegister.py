import RPi.GPIO as GPIO

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