#!/usr/bin/env python3
import time
import socket
import pickle

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8080        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = pickle.loads(s.recv(1024))
    print('Received', repr(data))

    #  send
    # s.sendall(pickle.dumps([0, 1, [1,2,3,4,5]]))

    # receive
    data = pickle.loads(s.recv(1024))
    print('Received', repr(data))
    
    # sleep
    print('sleep 60s.')
    time.sleep(60)
    print('end sleep')