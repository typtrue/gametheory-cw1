import numpy as np
from random import choice
import scipy.optimize as sci_op

VALUES = dict()
MIXEDSTRAT = dict()

class Game(object):
    def __init__(self, V, Y, P):
        self.V = V
        self.Y = Y
        self.P = P
        VALUES[f"{V}{Y}{P}"] = None
    
    def createSubgame(self, V_i, Y_j, P_k):
        V = self.V.copy()
        Y = self.Y.copy()
        P = self.P.copy()
        V.remove(V_i)
        Y.remove(Y_j)
        P.remove(P_k)
        return Game(V, Y, P)

    def value(self):
        if len(self.V) == 1:
            val = self.P[0] * np.sign(self.V[0] - self.Y[0])
            VALUES[f"{self.V} {self.Y} {self.P}"] = val
            return val
        total = 0
        for P_k in self.P:
            MIXEDSTRAT[f"{len(self.P)}{P_k}"] = None
            X = np.zeros((len(self.V), len(self.Y)))
            for i, V_i in enumerate(self.V):
                for j, Y_j in enumerate(self.Y):
                    score = P_k * np.sign(V_i - Y_j)
                    gs = self.createSubgame(V_i, Y_j, P_k)
                    if gs.V == gs.Y:
                        X[i, j] = score
                    elif VALUES[f"{gs.V}{gs.Y}{gs.P}"] is not None:
                        X[i, j] = score + VALUES[f"{gs.V}{gs.Y}{gs.P}"]
                    elif VALUES[f"{gs.V}{gs.Y}{gs.P}"] is not None:
                        X[i, j] = score - VALUES[f"{gs.V}{gs.Y}{gs.P}"]
                    else:
                        val = gs.value()
                        VALUES[f"{gs.V}{gs.Y}{gs.P}"] = val
                        X[i, j] = score + val
            x, value = game_val_from_mat(X)
            MIXEDSTRAT[f"{len(self.P)}{P_k}"] = x
            total += value
        return total / len(self.P)


def game_val_from_mat(A):
    m = A.shape[0]
    ineq = np.zeros((m, m + 1))
    k = np.ones(m)
    ineq[:, :m] = -A
    ineq[:, m] = k
    b_ineq = np.zeros(m)

    eq = np.ones((1, m + 1))
    eq[0, -1] = 0
    b_eq = np.ones((1, 1))

    c = np.zeros(m + 1)
    c[-1] = -1

    bounds = [(0, None) for i in range(m)]
    bounds.append((None, None))
    b_tup = tuple(bounds)

    res = sci_op.linprog(c, ineq, b_ineq, eq, b_eq, b_tup)

    return res.x[:-1], res.x[-1]

V = [1, 2, 3, 4, 5]
Y = [1, 2, 3, 4, 5]
P = [1, 2, 3, 4, 5]

g = Game(V, Y, P)
print(g.value())
print(MIXEDSTRAT[f"{len(P)}{2}"])