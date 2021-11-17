import numpy as np


def globalMinCut(A):
    assert A.shape[0] == A.shape[1]
    A = np.copy(A)
    inf = 1e9
    n = A.shape[0]
    co = [[i] for i in range(n)]
    opt_w = inf
    opt_cut = []
    for ph in range(1, n):
        w = np.copy(A[0])
        s = t = 0
        for it in range(n - ph):
            w[t] = -inf
            s = t
            t = w.argmax()
            w += A[t]
        if w[t] - A[t, t] < opt_w:
            opt_w = w[t] - A[t, t]
            opt_cut = co[t]
        co[s].extend(co[t])
        A[s, :] += A[t, :]
        A[:, s] = A[s, :]
        A[0, t] = -inf
    return opt_w, opt_cut


# A = np.array([[0, 3, 3, 4],
#               [3, 0, 9, 2],
#               [3, 9, 0, 1],
#               [4, 2, 1, 0]])

# A = np.zeros((8, 8))
# A[0, 1] = 2
# A[0, 4] = 3
# A[1, 2] = 3
# A[1, 4] = 2
# A[1, 5] = 2
# A[2, 3] = 4
# A[2, 6] = 2
# A[3, 6] = 2
# A[3, 7] = 2
# A[4, 5] = 3
# A[5, 6] = 1
# A[6, 7] = 3
# A = A + A.transpose()
# print(A)

# w, cut = globalMinCut(A)
# print(w)
# print(cut)


# T = int(input())
# for i in range(T):
#     n = int(input())
#     m = int(input())
#     A = np.zeros((n, n))
#     for j in range(m):
#         s = input().split()
#         a = int(s[0])
#         b = int(s[1])
#         c = int(s[2])
#         A[a - 1, b - 1] = A[b - 1, a - 1] = c
#     w, cut = globalMinCut(A)
#     print("Case " + str(i + 1) + ": " + str(w))

