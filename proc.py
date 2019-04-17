from smpi import *
import time
import pickle

if __name__ == '__main__':
    SMPI_init()
    rank = SMPI_get_rank()
    size = SMPI_get_size()

    print('rank %d, size %d' % (rank, size))

    print('rank %d sleeping 10s...' % rank)
    time.sleep(10)
    print('rank %d woke up' % rank)

    if rank == 0:
        print('sending...')
        SMPI_send(1, ['hello', 'its', 'me'])
        print('sent')

    if rank == 1:
        print('rank %d sleeping another 10s...' % rank)
        time.sleep(10)
        print('rank %d woke up' % rank)
        
        msg = SMPI_recv(0)

        print('received: ', msg)

    SMPI_finalize()

