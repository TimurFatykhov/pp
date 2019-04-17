#!/usr/bin/env python3
import socket 
import select 
import sys 
import threading
import pickle
import argparse

# parse option with number of clients
parser = argparse.ArgumentParser()
parser.add_argument("--n", help="maximum of clients")
args = parser.parse_args()
MAX_NUM_OF_CLIENTS = int(args.n)

# create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# connect to socket
IP_address = '127.0.0.1'
Port = 8080
server.bind((IP_address, Port)) 
server.listen(100) 
  
list_of_clients = []
dict_of_clients = {} 

def clientthread(conn, addr, rank): 
    # send message with rank and size
    conn.send(pickle.dumps((rank, MAX_NUM_OF_CLIENTS))) 

    while True:
        message = conn.recv(2048)
        if message: 
            pickled_message = pickle.loads(message)

            from_rank = pickled_message[0]
            to_rank = pickled_message[1]
            type_msg = pickled_message[2]
            info = pickled_message[3]

            # print('from ' + str(from_rank))
            # print('to ' + str(to_rank))
            # print('type ' + str(type_msg))
            # print('info ' + str(info))

            # send to specified rank
            dict_of_clients[to_rank].sendall(message)
        else: 
            # message may have no content if the connection 
            # is broken, in this case we close the connection
            # end kill the thread
            
            # print('connections refused!')
            conn.close()
            return 0


num_of_clients = 0
threads = []
while True:
    conn, addr = server.accept() 
    
    list_of_clients.append(conn) 
    dict_of_clients[num_of_clients] = conn
  
    # prints the address of the user that just connected 
    # print(addr[0] + ':' + str(addr[1]) + " connected")
  
    # creates and individual thread for every user  
    # that connects 
    t = threading.Thread(target=clientthread, args=(conn, addr, num_of_clients))
    threads.append(t)
    t.start()

    num_of_clients += 1

    if num_of_clients == MAX_NUM_OF_CLIENTS:
        break

# wait until all threads is finished
for t in threads:
    t.join()

server.close()