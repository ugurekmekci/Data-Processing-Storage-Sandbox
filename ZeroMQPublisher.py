
import zmq, time, json
from random import randrange
import sys
import threading

context = zmq.Context()

#### pub ####
socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://*:5556")

#### sub ####
socket_sub = context.socket(zmq.SUB)
socket_sub.connect("tcp://localhost:5557")
data_filter = ""
data_filter = data_filter.decode('ascii')
socket_sub.setsockopt_string(zmq.SUBSCRIBE, data_filter)

is_ready_to_send = True

def send():
    global is_ready_to_send
    while True:
        if not is_ready_to_send:
            continue
        data_to_send_dict = { 'data' : time.time()}
        socket_pub.send_string(json.dumps(data_to_send_dict))
        is_ready_to_send = False

def recieve():
    global is_ready_to_send
    while True:
        recieved_string = socket_sub.recv_string()
        if recieved_string == 'OK':
            is_ready_to_send = True
        print('RECIEVED:', recieved_string)

threads = []
t_send = threading.Thread(target=send)
threads.append(t_send)
t_send.start()

t_recieve = threading.Thread(target=recieve)
threads.append(t_recieve)
t_recieve.start()
    
