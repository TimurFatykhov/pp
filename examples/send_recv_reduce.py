#!/usr/bin/env python3
from smpi import COMM_WORLD

if __name__ == '__main__':
    comm = COMM_WORLD()
    rank = comm.get_rank()
    size = comm.get_size()

    print('I am rank #%d, of %d' % (rank, size))

    if rank == 0:
        comm.send(to_rank = 1, message = 'hello')
    if rank == 1:
        print(comm.recv(from_rank = 0))

    print(comm.reduce(value = rank, root = 0, op='sum'))
    print(comm.reduce(value = [0, 1, 2], root = 0, op='sum'))