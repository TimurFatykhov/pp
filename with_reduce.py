#!/usr/bin/env python3
from smpi import *
import time
import pickle
import numpy as np

if __name__ == '__main__':
    SMPI_init()
    rank = SMPI_get_rank()
    size = SMPI_get_size()

    print('rank %d, size %d' % (rank, size))

    print('rank %d sleeping 5s...' % rank)
    time.sleep(5)
    print('rank %d woke up' % rank)

    arr = list(np.random.randint(0, 10, 5))
    print('my array is ', arr)
    res = SMPI_reduce(arr, 0, SMPI_MUL)

    if rank == 0:
        print('rank #%d, reduce result is ' % (rank), res)

    SMPI_finalize()

