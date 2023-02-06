import time

import RPi.GPIO as GPIO

PORT = 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PORT, GPIO.OUT)


def turn_on_led(on_duration, off_duration=1, count=1):
    i = 0
    while i < count:
        # set GPIO14 pin to HIGH
        GPIO.output(PORT, GPIO.HIGH)
        # show message to Terminal
        print("LED is ON")
        # pause for one second
        time.sleep(on_duration)

        # set GPIO14 pin to HIGH
        GPIO.output(PORT, GPIO.LOW)
        # show message to Terminal
        print("LED is OFF")
        # pause for one second
        time.sleep(off_duration)
        i += 1


def turn_off_led(off_duration=1):
    GPIO.output(PORT, GPIO.LOW)
    print("LED is OFF")
    time.sleep(off_duration)
