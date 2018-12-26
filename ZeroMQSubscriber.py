
import sys, json, zmq
import threading, p

#### sub ####
context = zmq.Context()
socket_sub = context.socket(zmq.SUB)
socket_sub.connect("tcp://localhost:5556")
data_filter = ""
data_filter = data_filter.decode('ascii')
socket_sub.setsockopt_string(zmq.SUBSCRIBE, data_filter)

#### pub ####
socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://*:5557")

is_ready_to_recieve = True

def send():
    global is_ready_to_recieve
    while True:
        socket_pub.send_string('OK')
        is_ready_to_recieve = True

def recieve():
    global is_ready_to_recieve
    while True:
        if not is_ready_to_recieve:
            continue
        recieved_string = socket_sub.recv_string()
        is_ready_to_recieve = False
        print('RECIEVED:', recieved_string)

threads = []
t_send = threading.Thread(target=send)
threads.append(t_send)
t_send.start()

t_recieve = threading.Thread(target=recieve)
threads.append(t_recieve)
t_recieve.start()
