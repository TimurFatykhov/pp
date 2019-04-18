#!/usr/bin/env python3
import socket
import pickle
import numpy as np
import threading
from multiprocessing import Process, Queue
import sys

def __isend__(conn, message, que):
    message = pickle.dumps(message)
    conn.sendall(message)
    que.put('confirmed')


def __irecv__(conn, que):
    data = b""
    while True:
        batch = conn.recv(4096)
        if not batch: 
            break
        data += batch

    data = pickle.loads(data)
    que.put(data)


class COMM_WORLD():
    def __init__(self, host='127.0.0.1', port=61200):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        msg = s.recv(4096)
        msg = pickle.loads(msg) # parse
        s.close()

        addr = msg[0]
        self.my_ip = addr[0]
        self.my_port = addr[1]

        self.rank = int(msg[1])
        self.size = int(msg[2])

        # extract list of listening ranks
        listening_list = msg[3] # [rank, addr]

        # print('rank | listening', self. rank, listening_list)

        # connect to all waiting proceses
        self.world = {}
        for i, peer_addr in listening_list:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer_addr[0], peer_addr[1]))
            self.world[i] = [s, peer_addr[0], peer_addr[1]]
        

        # create server for listening other ("older") processes
        if self.rank + 1 < self.size:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.my_ip, self.my_port)) 
            server.listen(self.size)  
            for i in range(self.rank + 1, self.size):
                conn, addr = server.accept() 
                self.world[i] = [conn, addr[0], addr[1]]

        # print('rank | world', self. rank, self.world)
        

    def get_rank(self):
        return self.rank


    def get_size(self):
        return self.size

    
    def send(self, to_rank, message):
        message = pickle.dumps(message)
        self.world[to_rank][0].sendall(message)
        return 0


    def recv(self, from_rank):
        # message = 
        # print('size ', sys.getsizeof(message))
        # data = b""
        # while True:
        #     print("#1111111")
        #     batch = self.world[from_rank][0].recv(4096)
        #     print("#2222222")
        #     if not batch: 
        #         break
        #     data += batch

        data = self.world[from_rank][0].recv(4096)
        if data:
            data = pickle.loads(data)
            return data
        else:
            return None

    
    def reduce(self, value, root, op='sum'):
        """
        Parameters:
        -----------
        - value: array-like or scalar value

        - root: integer
            result of reduction will be sent to root process

        - op: string
            type of reduce operation
            possible values: 
                - 'sum'
                - 'prod'
        """

        if self.rank != root:
            print('#%d i am sending' % self.rank)
            self.send(to_rank = root, message = value)
            print('#%d i sent' % self.rank)
        else:
            values = []
            values.append(value)

            # receive arrays from other ranks
            for i in range(self.size):
                if i == self.rank:
                    continue # skip itself
                print('wait from %d' % i)
                values.append(self.recv(from_rank = i))
                print('received from %d' % i)

            
            if hasattr(value, '__iter__'):
                # if value is array-like
                values = np.stack(values)
                print(values)
            else:
                # if value is scalar
                values = np.array(values)
            
            if op == 'sum':
                return np.sum(values, 0)
            
            if op == 'prod':
                return np.prod(values, 0)

        return None


    def isend(self, to_rank, message):
        que = Queue()
        p = Process(target=__isend__, args=(self.world[to_rank][0], message,que))
        p.start()

        def wait():
            return que.get()

        que.wait = wait
        return que


    def irecv(self, from_rank):
        que = Queue()
        p = Process(target=__irecv__, args=(self.world[from_rank][0], que))
        p.start()

        def wait():
            return que.get()

        que.wait = wait
        return que

    
    def allgather(self, value):
        result = []
        
        for r in range(self.size):
            for p in range(self.size):
                if (p != r): # сами с собой не взаимодействуем
                    if (r == self.rank): # r шлет p и ждет ответ
                        print('r, p',r,p)
                        print('#1')
                        self.send(to_rank = p, message = value)
                        print('#1.2')
                        result.append(self.recv(from_rank = p))
                        print('#1 end')
                        
                    if (p == self.rank): # p слушает r и отвечает
                        print('p, r',p,r)
                        print('#2')
                        result.append(self.recv(from_rank = r))
                        print('#2.2')
                        self.send(to_rank = r, message = value)
                        print('#2 end')

        result.insert(self.rank, value)

        return result