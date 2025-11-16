from utils import *
import numpy as np
import matplotlib.pyplot as plt

#------------

Q = { 1: [[1]]}

def unique_decomp(N):
    try:
        return q[N]
    except:
        pass

    result = [[N]]

    for i in range(1, N):
        a = N - i 
        R = unique_decomp(i)
        for r in R:
            if r[0] <= a:
                result.append([a] + r)
    
    return [sorted(lis) for lis in result if len(lis) == len(set(lis))]


def check_best_selection(N, k, P=None):
    sets = unique_decomp(k)
    sets = [s for s in sets if len(s) == N]
    M = len(sets)
    X = np.zeros((M, M))
    if P == None:
        P = list(range(1, N+1))
    for i in range(M):
        print(f"{i}/{M}")
        for j in range(i):
            G = Game(sets[i], sets[j], P)
            X[i, j] = G.value()
    X -= X.T
    return game_val_from_mat(X)

k = 21
N = 2

J = unique_decomp(k)
J = [s for s in J if len(s) == N]
print(J)

res = check_best_selection(N, k)
print(res[0])
print(res[1])