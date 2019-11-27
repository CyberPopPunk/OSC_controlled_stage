""" 
11/12/19
Door Relay controls
Takes in sys args called from main program to open/ close/ malfunction door locks
flips GPIO #4, 17, 27, 22
"""
# TODO: figure out why when I set the pin low the relay lights come on. Are the lights to signify relay is swtiched? does GPIO set to LOW send signal? Find out next time on Dragon Ball Z!!!!!
# It functions this way because when the pins go to ground it allows the current to flow through to appropriate relay turning it 'on' when the pin is 'off'

from time import sleep
import RPi.GPIO as GPIO
from sys import argv
import random
#TODO setup logging

GPIO.setmode(GPIO.BCM)

pin_list = [4, 17, 27,22]
GPIO.setup(pin_list, GPIO.OUT)
    
def lock_control(mode, duration = 10):
    'takes an input mode and either locks, unlocks or glitches the relays controlling door locks.'
    if mode == 'lock':
        for pin in pin_list:
            GPIO.output(pin, True)
            print("Pin {} is set HIGH".format(pin))
            sleep(0.3)
    elif mode == 'unlock':
        for pin in pin_list:
            GPIO.output(pin, False)
            print("Pin {} is set LOW".format(pin))
    elif mode == 'haywire':
        for second in range(duration):
            for pin in pin_list:
                GPIO.output(pin,bool(random.getrandbits(1)))
                sleep(random.uniform(0.1, 0.3))
    #logging.debug('doors are {}'.format(mode))
    
    # no GPIO cleanup becuase I need them to keep state in main program. main program will have celanup at end.
    #GPIO.cleanup()

if __name__ == "__main__":
    try:
        lock_control(argv[1], int(argv[2]))
    except:
        lock_control(argv[1])