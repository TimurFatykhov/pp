# semi mpi
import socket
import pickle

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