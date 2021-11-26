import numpy as np
from readtxt import read_txt


# nearest neighbour heuristic, starting from node s
def nearest_neighbour(A, s):
    n = A.shape[0]
    T = [s]
    for i in range(n - 1):
        d = 1e9
        k = -1
        for j in range(n):
            if j not in T:
                if A[T[-1], j] < d:
                    d = A[T[-1], j]
                    k = j
        T.append(k)
    return T


# helper function for 2-opt
def reorder(T, t1, t2, t3, t4):
    n = len(T)
    A = []
    i = t4
    while True:
        A.append(T[i])
        if i == t2:
            break
        i = (n + i - 1) % n
    B = []
    i = t3
    while True:
        A.append(T[i])
        if i == t1:
            break
        i = (i + 1) % n
    A.extend(B)
    return A


# compute the cost of a tour
def cost(A, T):
    n = len(T)
    sam = 0
    for i in range(n):
        sam = sam + A[T[i], T[(i + 1) % n]]
    return sam


# T = [0, 1, 2, 3, 4, 5, 6]
# T_new = reorder(T, 1, 2, 4, 3)
# print(T_new)

# 2-opt heuristic
def two_opt(A, T):
    n = A.shape[0]
    while True:
        improved = False
        for i in range(n):
            t1 = i
            t2 = (i + 1) % n
            t3 = -1
            t4 = -1
            for j in range(n):
                if j != t1 and j != t2 and (n + j - 1) % n != t1 and (n + j - 1) % n != t2:
                    t3 = j
                    t4 = (n + j - 1) % n
                    if A[T[t1], T[t2]] + A[T[t3], T[t4]] > A[T[t2], T[t3]] + A[T[t4], T[t1]]:
                        break
                    else:
                        t3 = t4 = -1
            if t3 != -1:
                T = reorder(T, t1, t2, t3, t4)
                improved = True
                break
        if not improved:
            break
    return T

# A = read_txt("pr76.txt")
# tc = 1e9
# T = []
# for i in range(A.shape[0]):
#     NNT = nearest_neighbour(A, i)
#     S = two_opt(A, NNT)
#     if cost(A, S) < tc:
#         tc = cost(A, S)
#         T = S
#
# print(cost(A, T))
