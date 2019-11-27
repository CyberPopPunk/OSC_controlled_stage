""" 
11/12/19
Door Relay controls
Takes in sys args called from main program to open/ close/ malfunction door locks
flips GPIO #4, 17, 27, 22
"""

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pin_list = [4, 17, 27, 22]
sleep_time = 0.5

for pin in pin_list:
    GPIO.setup(pin, GPIO.OUT, initial = GPIO.LOW)
    print("Pin {} is on".format(pin))
    sleep(sleep_time)

state = True
while True:
    try:
        def cycle(value):
            for num, pin in enumerate(pin_list):
                if value ==  "HIGH":
                    GPIO.output(pin, GPIO.HIGH)
                else:
                    GPIO.output(pin, GPIO.LOW)
                print("Pin {} is off".format(pin))
                sleep(sleep_time)
        if state:
            cycle("HIGH")
        else:
            cycle("LOW")
        state = not state
            
    except KeyboardInterrupt:
        print("Quitting!")
        GPIO.cleanup()