from smpi import COMM_WORLD
import numpy as np
import time

time.sleep(5)

comm = COMM_WORLD()
rank = comm.get_rank()
size = comm.get_size()

"""
    Определяем параметры задачи
"""
# размерность матрицы
N = 100
# величина невязки, при которой закончим алгоритм
eps = 1e-5
# максимальное кол-во сделанных итераций
max_iter = 1000

"""
    Готовим матрицу (A), вектор-ответ (real_x) и правую часть (F)
"""
# инициализируем матрицу А
A = np.ones((N, N))
# заполнаяем диагональ значениями (2 * N + 1)
A += np.identity(len(A)) * 2 * N 
# настоящий х, который будем искать
real_x = np.ones(N) * 3
# правая часть Ax=F
F = A.dot(real_x) # векторное произведение матрицы на вектор

"""
    Основной цикл программы
    Разделение делаем по элементам вектора x
"""
# размер задачи (куска вектора х) для каждого процесса
# N должно без остатка делиться на кол-во процессов!
task_size = N // size

# начальное приближение (заполняем нулями)
x_curr = np.zeros(N) # x_current (x_k)
x_next = np.zeros(N) # x_next (x_k+1)

# засекаем время вычислений
start_time = time.time()

# Счётчик итераций
iteration = 0

flag = True
while flag:
    # определяем невязку куска
    bias = 0 
    # работаем с отведенным для процесса куском
    # определяем "границы работы"
    idx_from = rank * task_size
    idx_to = (rank + 1)*task_size

    for i in range(idx_from, idx_to): # range(откуда, докуда)
        summ = 0
        # считаем сумму (см в формуле)
        for j in range(N):
            summ += A[i, j] * x_curr[j]
        # считаем разность (см в формуле)
        sub = F[i] - summ
        # считаем невязку одного элемента
        bias += sub * sub

        x_next[i] = x_curr[i] + sub / A[i][i]
    
    # вставляем посчитанный кусок в нужное место
    x_curr[idx_from : idx_to] = x_next[idx_from : idx_to]
    
     # отправляем кусок следующего приближения другим процессам
    for r in range(size):
        for p in range(size):
            if (p != r): # сами с собой не взаимодействуем
                if (r == rank): # r взаимодействует с p
                    comm.send(to_rank = p, message = x_next[idx_from : idx_to])
                    x_new_part = comm.recv(from_rank = p)
                    x_curr[p * task_size : (p + 1)*task_size] = x_new_part
                if (p == rank): # p в ответ взаимодействует с r
                    x_new_part = comm.recv(from_rank = r)
                    x_curr[r * task_size : (r + 1)*task_size] = x_new_part
                    comm.send(to_rank = r, message = x_next[idx_from : idx_to])

    # УРА! МЫ ЗАВЕРШИЛИ ИТЕРАЦИЮ, ТЕПЕРЬ НАДО ПОСЧИТАТЬ НЕВЯЗКУ
    # складываем частичные невязки по всем процессам и отправляем
    # результат в нулевой процесс (root)
    result_bias = comm.reduce(value = bias, root = 0, op = 'sum')
 
    # теперь у нулевого процесса в "result_bias" лежит общая невязка
    if rank == 0:
        # если невязка ниже заданного уровня, то перестаем считать
        # приближения, ответ найден! и он лежит в любом из процессов!
        # изегаем зацикливания ограничением по количеству итераций
        if result_bias < eps or iteration >= max_iter:
            flag = False

        # отправляем всем процессам новое значение флага
        for r in range(size):
            if r == rank:
                # самому себе не отправляем
                continue

            comm.send(to_rank = r, message = flag)

    if rank != 0:
        # ждем от нулевого ранга новое значение флага
        flag = comm.recv(from_rank = 0)

print("\n\nrank = " + str(rank) + "\nx =\n" + str(x_curr) + "\ntime = " + str(time.time() - start_time) + " s")