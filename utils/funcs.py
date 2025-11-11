import numpy as np
from random import choice

VALUES = dict()

class Game(object):
    def __init__(self, V, Y, P):
        self.V = V
        self.Y = Y
        self.P = P
        VALUES[V, Y, P] = None
    
    def createSubgame(self, V_i, Y_j, P_k):
        V = self.V.remove(V_i)
        Y = self.Y.remove(Y_j)
        P = self.P.remove(P_k)
        return Game(V, Y, P)

    def value(self):
        total = 0
        for P_k in self.P:
            X = np.zeros(len(self.V), len(self.Y))
            for i, V_i in enumerate(self.V):
                for j, Y_j in enumerate(self.Y):
                    score = P_k * np.sign(V_i - Y_j)
                    gs = self.createSubgame(V_i, Y_j, P_k)
                    if VALUES[gs.V, gs.Y, gs.P] is not None:
                        X[i, j] = score + VALUES[gs.V, gs.Y, gs.P]
                    elif VALUES[gs.Y, gs.V, gs.P] is not None:
                        X[i, j] = score + VALUES[gs.Y, gs.V, gs.P]
                    else:
                        val = gs.value()
                        VALUES[gs.V, gs.Y, gs.P] = val
                        X[i, j] = score + val
            total += game_val_from_mat(X)
        return total / len(self.P)


def game_val_from_mat(A):
    raise NotImplementedError