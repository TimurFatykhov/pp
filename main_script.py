#!/usr/bin/env python3
from smpi import COMM_WORLD
import time
import pickle
import numpy as np

N = 6

if __name__ == '__main__':
    comm = COMM_WORLD()
    rank = comm.get_rank()
    size = comm.get_size()
    
    if rank != 0:
        # производим вычисления если ранг не 0
        my_A = np.ones( (N, N//(size-1)) ) * rank
        my_x = np.ones(N//(size-1)) * 3

        print('rank', rank)
        print(my_A)

        prod = my_A[0, :].dot(my_x)
        req = comm.isend(to_rank = 0, message = prod)
        for i in range(1, N):
            prod = my_A[i, :].dot(my_x)
            req.wait()
            req = comm.isend(to_rank = 0, message = prod)
        print('%d check #1' % rank)
        req.wait()
        print('%d check #2' % rank)
    else:
        # собираем результат если ранг 0
        print(rank, 'started')
        result = np.zeros(N)
        for i in range(N):
            print('hello', i)
            req1 = comm.irecv(from_rank = 1)
            req2 = comm.irecv(from_rank = 2)
            # print('wai1',req1.wait())
            # print('wai2',req2.wait())
            result[i] += req1.wait()
            result[i] += req2.wait()
            print('bye', i)
        
        print(rank, 'finished')

        print(result)