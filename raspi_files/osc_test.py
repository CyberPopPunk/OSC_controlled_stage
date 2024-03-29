import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

def print_volume_handler(unused_addr, args, volume):
    print("[{0}] ~ {1}".format(args[0], volume))
    
def print_compute_handler(unused_addr, args, volume):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](volume)))
    except ValueError: pass
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="192.168.0.30", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="the port to listen on")
    args = parser.parse_args()
    
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/filter", print)
    dispatcher.map("/volume", print_volume_handler, "Volume")
    dispatcher.map("/logvolume", print_compute_handler, "log volume", math.log)
    
    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("serving on {}".format(server.server_address))
    server.serve_forever()