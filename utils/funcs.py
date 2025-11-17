import numpy as np
import glpk

class Game(object):
    """
    Handles processing of instances of Goofspiel in order to calculate
    their value as well as optimal mixed strategies.
    """
    def __init__(self, V, Y, P, *, values=None):
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
        if values is None:
            self.VALUES = dict()
        else:
            self.VALUES = values
        self.MIXEDSTRAT = dict()
    
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
        # check for terminating condition
        if len(self.V) == 1:
            val = self.P[0] * np.sign(self.V[0] - self.Y[0])
            self.VALUES[f"{self.V}{self.Y}{self.P}"] = val
            return val
        total = 0
        # average all possible cards that could be drawn
        for P_k in self.P:
            X = np.zeros((len(self.V), len(self.Y)))

            # cosntruct payoff matrix using values of subgames (previously stored)
            for i, V_i in enumerate(self.V):
                for j, Y_j in enumerate(self.Y):
                    score = P_k * np.sign(V_i - Y_j)
                    gs = self.createSubgame(V_i, Y_j, P_k)

                    for key, val in gs.VALUES:
                        self.VALUES[key] = val

                    for key, val in gs.MIXEDSTRAT:
                        self.MIXEDSTRAT[key] = val

                    if gs.V == gs.Y:
                        X[i, j] = score
                        continue

                    try:
                        X[i, j] = score + self.VALUES[f"{gs.V}{gs.Y}{gs.P}"]
                        next
                    except:
                        pass

                    try:
                        X[i, j] = score - self.VALUES[f"{gs.Y}{gs.V}{gs.P}"]
                        continue
                    except:
                        val = gs.value()
                        self.VALUES[f"{gs.V}{gs.Y}{gs.P}"] = val
                        X[i, j] = score + val
            
            if X.shape == (2, 2):
                if X[0,0] >= X[0,1] and X[0,0] <= X[1,0]:
                    value = X[0,0]
                elif X[0,1] >= X[0,0] and X[0,1] <= X[1,1]:
                    value = X[0,1]
                elif X[1,0] >= X[1,1] and X[1,0] <= X[0,0]:
                    value = X[1,0]
                elif X[1,1] >= X[1,0] and X[1,1] <= X[0,1]:
                    value = X[1,1]
                else:
                    value = (X[0,0]*X[1,1] - X[0,1]*X[1,0]) / (X[0,0] + X[1,1] - X[0,1] - X[1,0])
            else:
                x, value = game_val_from_mat(X)
                self.MIXEDSTRAT[f"{self.V}{self.P}{P_k}"] = x
            total += value
        self.VALUES[f"{self.V}{self.Y}{self.P}"] = total / len(self.P)
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

    # init optimisation problem

    M = A.shape[0]
    lp = glpk.LPX()

    lp.obj.maximize = True
    lp.rows.add(M + 1)
    lp.cols.add(M + 1)

    for r in lp.rows[:-1]:
        r.bounds = 0.0, None
    lp.rows[-1].bounds = 1.0

    for c in lp.cols[:-1]:
        c.bounds = 0.0, None
    lp.cols[-1].bounds = None, None

    lp.obj[:] = list(np.zeros(M + 1, dtype=float))
    lp.obj[-1] = 1.0

    mat = np.zeros((M+1, M+1))
    mat[:-1, :-1] = A
    mat[-1, :-1] = np.ones(M)
    mat[:-1, -1] = -np.ones(M)

    mat.flatten()

    lp.matrix = list(mat.flatten())

    lp.simplex()

    vec = [c.primal for c in lp.cols[:-1]]

    return vec, lp.obj.value

# V = [1, 2, 3, 4, 5, 6]
# Y = [1, 2, 3, 4, 5, 6]
# P = [1, 2, 3, 4, 5, 6]

# G = Game(V, Y, P)
# print(G.value())
# print(G.MIXEDSTRAT[f"{V}{P}{3}"])