#!/usr/bin/env python3
from smpi import COMM_WORLD
import time
import pickle
import numpy as np

N = 500

if __name__ == '__main__':
    comm = COMM_WORLD()
    rank = comm.get_rank()
    size = comm.get_size()
    
    start_time = time.time()

    if rank != 0:
        # производим вычисления если ранг не 0
        my_A = np.ones( (N, N//(size-1)) ) * rank
        my_x = np.ones(N//(size-1)) * 3

        # print('rank', rank)
        # print(my_A)

        prod = my_A[0, :].dot(my_x)
        req = comm.isend(to_rank = 0, message = prod)
        for i in range(1, N):
            prod = my_A[i, :].dot(my_x)
            req.get()
            req = comm.isend(to_rank = 0, message = prod)
        req.get()
    else:
        # собираем результат если ранг 0
        result = np.zeros(N)
        for i in range(N):
            req1 = comm.irecv(from_rank = 1)
            req2 = comm.irecv(from_rank = 2)
            r1 = req1.get()
            if r1 is not None:
                result[i] += r1

            r2 = req2.get()
            if r2 is not None:
                result[i] += r2
        
        finish_time = time.time()
        print('time : ', finish_time - start_time)
        print('N ',len(result))
