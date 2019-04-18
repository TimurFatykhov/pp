#!/usr/bin/env python3
from smpi import COMM_WORLD

if __name__ == '__main__':
    comm = COMM_WORLD()
    rank = comm.get_rank()
    size = comm.get_size()

    print('I am rank #%d, of %d' % (rank, size))

    if rank == 0:
        req = comm.isend(1, [0.1]*3000000)

        print('rank #%d already here' % rank)
        req.wait()
    if rank == 1:
        req = comm.irecv(0)

        print('rank #%d already here :)' % rank)
        print(len(req.wait()))
    

    print('rank #%d is waiting...' % rank)