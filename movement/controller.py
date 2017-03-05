import RPi.GPIO as GPIO
import json


class Controller:
    """
    This class will control the steering and throttle
    of the remote control car.
    """

    def __init__(self):
        with open('config.json') as json_data_file:
            self.config = json.load(json_data_file)

        if self.config["gpioMode"] == "board":
            GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.setmode(GPIO.BCM)

        self.steeringGPIO = self.config["steering"]["channel"]
        self.steeringFrequency = self.config["steering"]["frequency"]
        self.steering = GPIO.PWM(self.steeringGPIO, self.steeringFrequency)
        self.steeringLeft = self.config["steering"]["left"]
        self.steeringCenter = self.config["steering"]["center"]
        self.steeringRight = self.config["steering"]["right"]
        self.steeringInterval = (self.steeringRight - self.steeringLeft) / 10.0
        self.steeringCurrent = self.steeringCenter

        self.throttleGPIO = self.config["throttle"]["channel"]
        self.throttleFrequency = self.config["throttle"]["frequency"]
        self.throttle = GPIO.PWM(self.throttleGPIO, self.throttleFrequency)
        self.throttleReverse = self.config["throttle"]["reverse"]
        self.throttleStop = self.config["throttle"]["stop"]
        self.throttleForward = self.config["throttle"]["forward"]
        self.throttleInterval = (self.throttleForward - self.throttleReverse) \
            / 10.0
        self.throttleCurrent = self.throttleStop

    def __enter__(self):
        """
        Starts the GPIO pins a' turnin
        """

        self.steering.start(self.steeringCurrent)
        self.throttle.start(self.throttleCurrent)
        return self

    #####################################
    # Steering
    #####################################
    def steer(self, interval=0):
        self.steeringCurrent = self.steeringCurrent + interval
        if self.steeringCurrent < self.steeringLeft:
            self.steeringCurrent = self.steeringLeft
        elif self.steeringCurrent > self.steeringRight:
            self.steeringCurrent = self.steeringRight

        self.steering.ChangeDutyCycle(self.steeringCurrent)

    def steerCenter(self):
        self.steeringCurrent = self.steeringCenter
        self.steer()

    def steerLeft(self, interval=None):
        if interval is None:
            interval = -1.0 * self.steeringInterval
        if interval > 0:
            interval = -1.0 * interval
        self.steer(interval)

    def steerLeftMax(self):
        self.steeringCurrent = self.steeringLeft
        self.steer()

    def steerRight(self, interval=None):
        if interval is None:
            interval = self.steeringInterval
        if interval < 0:
            interval = -1.0 * interval
        self.steer(interval)

    def steerRightMax(self):
        self.steeringCurrent = self.steeringRight
        self.steer()

    #####################################
    # Driving
    #####################################
    def drive(self, interval=0):
        self.throttleCurrent = self.throttleCurrent + interval
        if self.throttleCurrent < self.throttleReverse:
            self.throttleCurrent = self.throttleReverse
        elif self.throttleCurrent > self.throttleForward:
            self.throttleCurrent = self.throttleForward

        self.throttle.ChangeDutyCycle(self.throttleCurrent)

    def driveStop(self):
        self.throttleCurrent = self.throttleStop
        self.drive()

    def driveForward(self, interval=None):
        if interval is None:
            interval = -1.0 * self.throttleInterval
        if interval > 0:
            interval = -1.0 * interval
        self.drive(interval)

    def driveForwardMax(self):
        self.throttleCurrent = self.throttleForward
        self.drive()

    def driveBackwards(self, interval=None):
        if interval is None:
            interval = self.throttleInterval
        if interval < 0:
            interval = -1.0 * interval
        self.drive(interval)

    def driveBackwardsMax(self):
        self.throttleCurrent = self.throttleReverse
        self.drive()

    def __exit__(self, exc_type, exc_value, traceback):
        self.steering.stop()
        self.throttle.stop()
        GPIO.cleanup()
        return False
