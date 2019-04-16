# semi mpi
import socket
import pickle
import numpy as np
import threading

rank = None
size = None
socket_to_server = None

receive_buffer = {}

def __connect_to_server__(host='127.0.0.1', port=8080):
    """
    Returns:
    --------
    - s: connected socket
        now you can use s.sendall(), s.recv()
    """
    global rank, size

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    msg = s.recv(1024)
    msg = pickle.loads(msg)

    rank = int(msg[0])
    size = int(msg[1])

    return s

def SMPI_init():
    global socket_to_server
    socket_to_server = __connect_to_server__()

    for i in range(size):
        receive_buffer[i] = []


def SMPI_get_rank():
    return rank


def SMPI_get_size():
    return size


def SMPI_send(to_rank, message):
    """
    To be honest this function is SMPI_isend
    """
    msg_to_send = [rank, to_rank, message]
    msg_to_send = pickle.dumps(msg_to_send)
    socket_to_server.sendall(msg_to_send)


def SMPI_recv(from_rank):
    # if we have messages in buffer from this rank, 
    # then return first message in queue
    if receive_buffer[from_rank]:
        return receive_buffer[from_rank].pop(0)

    while True:
        msg_received = socket_to_server.recv(1024)
        msg_received = pickle.loads(msg_received)

        recv_from = msg_received[0]
        to_rank = msg_received[1]
        clear_msg = msg_received[2]

        if to_rank != rank:
            ValueError('Message was sent to another rank!')

        if from_rank != recv_from:
            # if message was sent from another rank,
            # then put it into buffer
            receive_buffer[recv_from].append(clear_msg)
        else:
            return msg_received


def SMPI_finalize():
    socket_to_server.close()

SMPI_SUM, SMPI_MUL = 1, 2
def SMPI_reduce(array, root, op):
    arrays = []
    if rank == root:
        arrays.append(array)

        # receive arrays from other ranks
        for i in range(size):
            if i == rank:
                # skip itself
                continue

            arrays.append(SMPI_recv(i)[2]) # [2] - store the message (array)
    
        if op == SMPI_SUM:
            return list(np.sum(arrays, 0))
        
        if op == SMPI_MUL:
            return list(np.prod(arrays, 0))
    else:
        SMPI_send(root, array)
        return 0


#########################################################################
######################### "Non-stop" functions ##########################
"""
SMPI_ITYPE_RECV and SMPI_ITYPE_SEND we will use
like tag for i_buffer records to distinguish if it
delivery confirmation (for isend), or received message
(for irecv)
"""
SMPI_ITYPE_RECV, SMPI_ITYPE_SEND = 0, 1

"""
key - i_id
value - message
"""
i_buffer = {}

def __irecv__(from_rank, i_id):
    # if we have messages in buffer from this rank, 
    # then return first message in queue
    if receive_buffer[from_rank]:
        i_buffer[i_id] = receive_buffer[from_rank].pop(0)

    while True:
        msg_received = socket_to_server.recv(1024)
        msg_received = pickle.loads(msg_received)

        recv_from = msg_received[0]
        to_rank = msg_received[1]
        clear_msg = msg_received[2]

        if to_rank != rank:
            ValueError('Message was sent to another rank!')

        if from_rank != recv_from:
            # if message was sent from another rank,
            # then put it into buffer
            receive_buffer[recv_from].append(clear_msg)
        else:
            i_buffer[i_id] = clear_msg
            return 0


def SMPI_irecv(from_rank, i_id):
    """
    Parameters:
    -----------
    - from_rank : integer
    - i_id : integer
    """
    t = threading.Thread(target=__irecv__, args=(from_rank, i_id))
    t.start()
    return 0


def __isend__(to_rank, message, i_id):
    msg_to_send = [rank, to_rank, message]
    msg_to_send = pickle.dumps(msg_to_send)
    socket_to_server.sendall(msg_to_send)

    msg_received = socket_to_server.recv(1024)
    msg_received = pickle.loads(msg_received)


def SMPI_isend(to_rank, message, i_id):
    """
    Parameters:
    -----------
    - to_rank : integer
    - message : any type
    - i_id : integer
    """
    t = threading.Thread(target=__isend__, args=(to_rank, message, i_id))
    t.start()
    return 0


def SMPI_wait(i_id):
    """
    Return resul of 'i'-operation: result SMPI_isend or SMPI_irecv
    """
    return i_buffer[i_id]
    




    



    # data = pickle.loads(s.recv(1024))
    # print('Received', repr(data))

    # print('sleep 10s.')
    # time.sleep(10)
    # print('end sleep')

    # #  send
    # s.sendall(pickle.dumps([0, 1, [1,2,3,4,5]]))

    # # receive
    # # data = pickle.loads(s.recv(1024))
    # # print('Received', repr(data))

    # # sleep
    # print('sleep 60s.')
    # time.sleep(60)
    # print('end sleep')