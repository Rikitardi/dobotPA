import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
while True:
    try:
        if GPIO.input(11) == 1:
            print("yes")
        elif GPIO.input(11) == 0:
            print("no")
        time.sleep(2)
    except KeyboardInterrupt:
        GPIO.cleanup()
