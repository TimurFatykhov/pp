#!/usr/bin/env python3
import socket 
import select 
import sys 
import threading
import pickle
import argparse
import time

NUM_OF_CLIENTS = None
VERBOSE = None

# parse option with number of clients
parser = argparse.ArgumentParser()
parser.add_argument("--n", help="maximum of clients")
parser.add_argument("--v", help="verbose")
args = parser.parse_args()

if args.v is None:
    VERBOSE = 0
else:
    VERBOSE = bool(args.n)

if args.n is None:
    NUM_OF_CLIENTS = 1
else:
    NUM_OF_CLIENTS = int(args.n)

# create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# connect to socket
IP_address = '127.0.0.1'
port = 61200
server.bind((IP_address, port)) 
server.listen(NUM_OF_CLIENTS) 

if VERBOSE:
    print('server is listening at %d' % port)

client_index = 0
clients_info = []
while client_index < NUM_OF_CLIENTS:
    conn, addr = server.accept() 

    # send message to client
    data_to_send = pickle.dumps([addr, client_index, NUM_OF_CLIENTS, clients_info])
    conn.sendall(data_to_send)

    # memorize info about all clients
    clients_info.append([client_index, addr])

    if VERBOSE:
        # prints the address of the user that was connected 
        print(addr[0] + ':' + str(addr[1]) + " has connected")

    conn.close()
    client_index += 1


server.close()