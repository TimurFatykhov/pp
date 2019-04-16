from smpi import *
import time
import pickle

if __name__ == '__main__':
    SMPI_init()
    rank = SMPI_get_rank()
    size = SMPI_get_size()

    print('rank %d, size %d' % (rank, size))

    print('sleeping...')
    time.sleep(3)
    print('end sleep')

    SMPI_finalize()

