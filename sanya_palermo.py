#!/usr/bin/env python3
from smpi import *
import time
import pickle
import numpy as np

N = 2

if __name__ == '__main__':
    SMPI_init()
    rank = SMPI_get_rank()
    size = SMPI_get_size()

    time.sleep(9)
    
    if rank != 0:
        # производим вычисления если ранг не 0
        my_A = np.ones( (N, N//(size-1)) ) * rank
        my_x = np.ones(N//(size-1)) * 3

        print('rank', rank)
        print(my_A)

        prod = my_A[0, :].dot(my_x)
        SMPI_isend(0, prod, 0)
        for i in range(1, N):
            prod = my_A[i, :].dot(my_x)
            SMPI_wait(i - 1)
            SMPI_isend(0, prod, i)
        SMPI_wait(N - 1)
    else:
        # собираем результат если ранг 0
        print(rank, 'started')
        result = np.zeros(N)
        for i in range(N):
            print('hello', i)
            SMPI_irecv(1, -1)
            SMPI_irecv(2, -2)
            result[i] += SMPI_wait(-1)
            result[i] += SMPI_wait(-2)
            print('bue', i)
        
        print(rank, 'finished')

        print(result)
        
    SMPI_finalize()

