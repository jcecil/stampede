import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT)

p = GPIO.PWM(33, 50)  # channel=12 frequency=50Hz
p.start(0)
try:
    while 1:
        for dc in range(0, 18, 1):
            p.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(2)

        for dc in range(8, 9, -1):
            p.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(2)

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()
