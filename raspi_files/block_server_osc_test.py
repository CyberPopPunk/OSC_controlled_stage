from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import sys

sys.path.insert(1, '/home/pi/Desktop/Solitary/scripts/raspi_files/doors')
sys.path.insert(1, '/home/pi/Desktop/Solitary/scripts/raspi_files/clock')
sys.path.insert(1, '/home/pi/Desktop/Solitary/scripts/raspi_files/fan')
sys.path.insert(1, '/home/pi/Desktop/Solitary/scripts/raspi_files/lights')

import doors
#import clock_input
import fan
import lights

def clock_handler(address, *args):
    print(f"{address}: {args}")
    import time
    import datetime
    from adafruit_ht16k33 import segments
    import busio
    import board
    
    # Create the I2C interface.
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the LED segment class.
    # This creates a 7 segment 4 character display:
    display = segments.Seg7x4(i2c)

    # clear display
    display.fill(0)


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

def clock_input(address, *args):
    pass

def doors_handler(address, *args):
    try:
        doors.lock_control(args[0], args[1])
    except:
        doors.lock_control(args[0])

def fan_handler(address, *args):
    fan.fan_control(args[0])
    
def lights_handler(address, *args):
    pass

dispatcher = Dispatcher()
dispatcher.map("/clock*", clock_handler)
dispatcher.map("/doors*", doors_handler)
dispatcher.map("/fan*", fan_handler)
dispatcher.map("lights*", lights_handler)
dispatcher.set_default_handler(default_handler)

ip = "192.168.0.30"
port = 5005

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever