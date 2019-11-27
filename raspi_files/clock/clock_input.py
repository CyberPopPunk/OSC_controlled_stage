import time
import datetime
import sys
import random
import logging
from adafruit_ht16k33 import segments
import board
import busio

logging.basicConfig(level=logging.DEBUG)
# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c)

def clock_specific(message):
    """Displays a specific string message of supported chars on the 7segDisplay."""
    for num, char in enumerate(message):
        display[num] = char
        
def blank_blink():
    """Makes the 7segDisplay all hyphens and they blink on and off every half second."""
    clock_specific('----')
    display.print(':')
    time.sleep(0.5)
    clear_clock()
    time.sleep(0.5)


def clear_clock():
    """Clears 7segDisplay to look like it's off."""
    display.fill(0)

def haywire(duration):
    """Generates random chars to appear on the 7segDisplay like glitching."""
    for seconds in range(duration):
        for digit in range(4):
            display[digit] =  random.choice('0124679abcdef_.-')
        time.sleep(random.random())
    clear_clock()
            

def timer(start_time, change_value, speed=1, step=1):
    """Makes 7segDisplay operate as a counter in base-10 numbers
    
    start(int) -- start value of timer 
    change_value(int) -- how much the value of start will change
    speed -- how fast in milliseconds for the step to change (must be positive).
    step -- amount of change per step (must be positive).
    """
    clock_specific(start_time)
    current_value = int(start_time)
    change_value = int(change_value)
    speed_millis_to_seconds = int(speed)/1000
    
    if change_value < 0:
        step = -step
    end_value = int(start_time) + change_value + step
    
    while current_value != end_value:
        display.print(current_value)
        time.sleep(speed_millis_to_seconds)
        current_value += step

#def clock(start_time, change_seconds, speed=1000):
def clock(start_time, end_time, speed=1000):
    """Makes 7segDisplay operate as a clock in 12-hr format
    
    start_time -- start minutes display
    start_seconds -- starting seconds display
    change_seconds -- amount of seconds change from start value.
    speed -- clock speed in seconds.
    """
    # start_minutes, start_seconds = input_time.split(':')
    # current_minutes = start_minutes
    # current_seconds = start_seconds
    # change_sign = 1
    # if int(change_seconds) < 0:
    #     change_sign = -1 
    
    # #calculate difference in seconds between start time and change_time
    # start_time = int(start_seconds) + int(start_minutes)*60
    # end_time = int(start_time) + int(change_seconds)
    
    # current_time = start_time
    # logging.debug("current  minutes: " + str(current_minutes))
    # logging.debug("current seconds: " + str(current_seconds))
    # logging.debug("start time: {}".format(start_time))
    # logging.debug("end time: {}".format(end_time))
    
    # start_minutes, start_seconds = input_time.split(':')
    # end_minutes, end_seconds = end_time.split(':')
    time_format = '%M:%S'
    
    start_time = datetime.datetime.strptime(start_time, time_format)
    end_time = datetime.datetime.strptime(end_time, time_format)
    # current_minutes = start_minutes
    # current_seconds = start_seconds
    current_time = start_time
    
    if start_time > end_time:
        difference = (start_time - end_time).seconds
        unit = datetime.timedelta(seconds=-1)
    else:
        difference = (end_time - start_time).seconds
        unit = datetime.timedelta(seconds=1)
    logging.debug("start time: {}".format(start_time))
    logging.debug('end time: {}'.format(end_time))
    logging.debug('difference: {}'.format(difference))
    
    #change_seconds = datetime.timedelta(seconds=int(change_seconds))
    
    # def seconds_to_minutes(seconds_to_convert):
    #     """Converts seconds difference between start and end times to minutes and seconds"""
    #     output_seconds = seconds_to_convert%60
    #     output_minutes = seconds_to_convert//60
    #     return output_minutes, output_seconds
    
    while (current_time != end_time + unit):
        # current_minutes, current_seconds = seconds_to_minutes(current_time)
        # logging.debug("current minutes: {}, current seconds: {}".format(current_minutes, current_seconds))
        # #print minutes and seconds ensuring 2 digits with zeros filled in
        # display.print(str(current_minutes).zfill(2)+str(current_seconds).zfill(2))
        display.print(str(current_time))
        display.print(':')
        logging.debug('current time: {}'.format(current_time))
        current_time = current_time + unit
        time.sleep(int(speed)/1000)

def realtime():
    """displays current realtime for specified duration"""
    # get system time
    now = datetime.datetime.now()
    hour = now.hour
    if hour > 12:
        hour = hour - 12
    minute = now.minute
    second = now.second

    # setup HH:MM for display and print it
    clock = '%02d%02d' % (hour,minute)          # concat hour + minute, add leading zeros
    display.print(clock)

    # Toggle colon when displaying time
    if second % 2:
        display.print(':')                      # Enable colon every other second
    else:
        display.print(';')                      # Turn off colon
    time.sleep(1)

#try error handling
  
#def parse_command(mode, param_1, param_2, param_3):
def parse_command(mode, **kwargs):
    """ Functino to parse the OSC related message for the clock input """
    #TODO: setup **kwargs for the inputs of the system
    # **kwargs stores inputs in a dictionary. Try a reverse lookup then parse by mode
    # will have to change the input from OSC for it to work
    # former OSC message: /clock timer 3:45 -20 3
    # new OSC messgae: /clock timer start_time=3:45 change_value=10
    
    mode = sys.argv[1]
    print("mode: {}".format(mode))
    print("Parameters: ")
    for item in sys.argv[2:]:
        print(item)

    clear_clock()

    if mode == 'blank':
        for seconds in range(int(kwargs['duration'])):
            blank_blink()

    elif mode == 'clock':
        input_time = kwargs['start']
        # if len(sys.argv) > 4:
        #     clock(input_time, sys.argv[3], sys.argv[4])
        # else:
        #     clock(input_time, sys.argv[3])
        try:
            clock(kwargs['start'], kwargs['end'], kwargs['speed'])
        except:
            clock(kwargs['start'], kwargs['end'])

    elif mode == 'timer':
        # start = kwargs['start']
        # change = kwargs['change']
        # speed = kwargs['speed']
        # step =  kwargs['step']
        try:
            timer(kwargs['start'], kwargs['change'], kwargs['speed'], kwargs['step'])
        except:
            try:
                timer(kwargs['start'], kwargs['change'], kwargs['speed'])
            except:
                timer(kwargs['start'], kwargs['change'])

    elif mode == 'haywire':
        haywire(int(kwargs['duration']))

    elif mode == 'specific':
        clock_specific(kwargs['message'])

    elif mode == 'realtime':
        realtime()

    elif mode == 'off':
        clear_clock()  

if __name__ == "__main__":
    
    input_kwargs = dict(arg.split('=') for arg in sys.argv[2:])
    for k, v in input_kwargs.items():
        print('keyword argument--> {}:{}'.format(k, v))
    parse_command(sys.argv[1], **input_kwargs)
    # """ EXAMPLE CODE (TURN THIS INTO AN ITERABLE)
    #         -- parse string args for key-value pairs and put them into a dict
    #         -- then pass dict to parse_command(mode, **{dict of inputs})
    #         keyword, sep, value = f.partition('=')
    #         kwargs = {keyword: value.strip('"')}
    #         d = Image.objects.filter(**kwargs)"""
    # #parse_command(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]) 

