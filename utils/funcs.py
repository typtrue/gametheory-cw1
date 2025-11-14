import numpy as np
from random import choice
import scipy.optimize as sci_op

VALUES = dict()
MIXEDSTRAT = dict()

class Game(object):
    """
    Handles processing of instances of Goofspiel in order to calculate
    their value as well as optimal mixed strategies.
    """
    def __init__(self, V, Y, P):
        """
        Initialise game based on three sets of input cards.
        
        Parameters
        ----------
        V : list of int
            List of Player 1's cards.
        Y : list of int
            List of Player 2's cards.
        P : list of int
            List of central cards.
        """
        self.V = V
        self.Y = Y
        self.P = P
        VALUES[f"{V}{Y}{P}"] = None
    
    def createSubgame(self, V_i, Y_j, P_k):
        """
        Create a subgame based on removing certain cards from each player.
        
        Parameters
        ----------
        V_i : int
            Card to be removed from Player 1's cards.
        Y_j : int
            Card to be removed from Player 2's cards.
        P_k : int
            Face-up central card to be removed.
        
        Returns
        -------
        G : Game
            Subgame created from removing specified cards.
        """
        V = self.V.copy()
        Y = self.Y.copy()
        P = self.P.copy()
        V.remove(V_i)
        Y.remove(Y_j)
        P.remove(P_k)
        return Game(V, Y, P)

    def value(self):
        """
        Calculate the value of game.

        Returns
        -------
        value : float
            Value of game.
        
        Yields
        ------
        MIXEDSTRAT : dict
            Holds optimal mixed strategies for a given subgame and upcard.
            Access using `MIXEDSTRAT[f"{len(P)}{P_k}"]`.
        """
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
            MIXEDSTRAT[f"{len(self.P)}{P_k}"] = x[::-1]
            total += value
        return total / len(self.P)


def game_val_from_mat(A):
    """
    Get a value of a game from a given payoff matrix `A`.

    Parameters
    ----------
    A : array_like
        Payoff matrix of game to calculate value of.

    Returns
    -------
    x : array_like
        Mixed strategy vector that produces highest payoff.
    v : float
        Value of game.
    """
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

V = [1, 2, 3, 4]
Y = [1, 2, 3, 4]
P = [1, 2, 3, 4]

g = Game(V, Y, P)
print(g.value())
print(MIXEDSTRAT[f"{len(P)}{2}"])