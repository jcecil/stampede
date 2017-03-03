import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 80)  # channel=12 frequency=50Hz
p.start(0)

try:
    while 1:
        for dc in range(10, 18, 1):
            p.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(0.1)

        for dc in range(18, 9, -1):
            p.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(0.1)

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()
