import numpy as np
from random import choice


class Game(object):
    def __init__(self, N, p1_cards, p2_cards):
        if len(p1_cards) != N or len(p2_cards) != N:
            raise ValueError(f"size of both players' decks must be {N}")
        self.N = N
        self.common = list(range(1, N+1))
        self.p1_cards = p1_cards
        self.p2_cards = p2_cards
        self.p1_score = 0
        self.p2_score = 0
        self.facecard = choice(self.common)
        self.gamewon = False

    def play(self, p1, p2):
        if p1 >= p2:
            self.p1_score += self.facecard
        if p2 >= p1:
            self.p2_score += self.facecard
        self.p1_cards.remove(p1)
        self.p2_cards.remove(p2)
        self.common.remove(self.facecard)
        if not self.common:
            self.gamewon = True
            return True
        self.facecard = choice(self.common)
        return False


g = Game(2, [1,2], [1,2])
g.play(1, 2)
print(g.p1_score, g.p2_score)
print(g.p1_cards, g.p2_cards, g.common)