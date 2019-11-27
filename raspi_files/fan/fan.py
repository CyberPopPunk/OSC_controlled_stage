import RPi.GPIO as GPIO
from time import sleep
import logging
from sys import argv

GPIO.setmode(GPIO.BCM)
signal_pin = 22
GPIO.setup(signal_pin, GPIO.OUT, initial=False)

def fan_control(mode):
    if mode == 'on':
        GPIO.output(signal_pin, False)
    elif mode == 'off':
        GPIO.output(signal_pin, True)
    else:
        raise ValueError('Invalid input: try "on" or "off"')
    # TODO: add logging to record status to file

if __name__ == "__main__":
    fan_control(argv[1])
