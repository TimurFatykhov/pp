#!/usr/bin/env python3
from smpi import *
import time
import pickle


if __name__ == '__main__':
    SMPI_init()
    rank = SMPI_get_rank()
    size = SMPI_get_size()

    print('rank %d, size %d' % (rank, size))

    print('rank %d sleeping 4s...' % rank)
    time.sleep(4)
    print('rank %d woke up' % rank)

    if rank == 0:
        print('sending...')
        SMPI_isend(1, ['hello', 'its', 'me'], i_id=0)
        print('sent')

        print('wait received ', SMPI_wait(i_id=0))

    if rank == 1:
        print('rank %d sleeping another 10s...' % rank)
        time.sleep(10)
        print('rank %d woke up' % rank)
        
        SMPI_irecv(0, i_id=1)

        print('wait received ', SMPI_wait(i_id=1))

    SMPI_finalize()

