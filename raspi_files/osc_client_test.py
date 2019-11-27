from pythonosc.udp_client import SimpleUDPClient
import sys

ip = "192.168.0.30"
port = 5005

client = SimpleUDPClient(ip, port)  # Create client

address_input =  sys.argv[1]
input_parameters = sys.argv[2:]

client.send_message(address_input, input_parameters)   # Send float message