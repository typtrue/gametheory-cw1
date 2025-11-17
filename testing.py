from utils import *
import numpy as np
import matplotlib.pyplot as plt
import time
import random

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
    
    return [lis for lis in result if len(lis) == len(set(lis))]


def check_best_selection(N, k, P=None):
    sets = unique_decomp(k)
    sets = [sorted(s) for s in sets if len(s) == N]
    M = len(sets)
    X = np.zeros((M, M))
    if P == None:
        P = list(range(1, N+1))
    vals = dict()
    times = []
    for i in range(M):
        print(f"{i}/{M}")
        for j in range(i):
            G = Game(sets[i], sets[j], P)
            t = time.time()
            X[i, j] = G.value()
            times.append(time.time() - t)
        if i > 0:
            run = times[max(len(times)-20, 0):]
            print(f"avg time per game: {sum(run)/len(run)}s")
    X -= X.T
    return game_val_from_mat(X), X, sets

k = 21
N = 5

res, _, sets = check_best_selection(N, k)
print(sets)
print(res[0])
