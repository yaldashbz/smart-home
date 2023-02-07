import time

import RPi.GPIO as GPIO

PORT = 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PORT, GPIO.OUT)


def turn_on_led(on_duration, off_duration=1, count=1):
    i = 0
    while i < count:
        GPIO.output(PORT, GPIO.HIGH)
        print("LED is ON")
        time.sleep(on_duration)

        GPIO.output(PORT, GPIO.LOW)
        print("LED is OFF")
        time.sleep(off_duration)
        i += 1


def turn_off_led(off_duration=1):
    GPIO.output(PORT, GPIO.LOW)
    print("LED is OFF")
    time.sleep(off_duration)
