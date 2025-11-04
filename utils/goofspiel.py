import numpy as np
from random import choice


class Game(object):
    def __init__(self, N, cards):
        if len(cards[0]) != N or len(cards[1]) != N:
            raise ValueError(f"size of both players' decks must be {N}")
        self.N = N
        self.common = list(range(1, N+1))
        self.players = [Player(self, c, i) for i, c in enumerate(cards)]
        self.face_up = choice(self.common)
        self.gamewon = False

    def play(self):
        moves = [p.move() for p in self.players]
        for i, p in enumerate(self.players):
            if moves[i] == max(moves):
                p.score += self.face_up
            p.cards.remove(self.face_up)
        self.common.remove(self.face_up)
        if not self.common:
            self.gamewon = True
            return int(self.players[1].score > self.players[0].score)
        self.face_up = choice(self.common)
        return False

class Player(object):
    def __init__(self, gamestate, cards, player_no):
        self.gamestate = gamestate
        self.id = player_no
        self.cards = cards
        self.score = 0

    def move(self):
        other = self.gamestate.players[1-self.id]
        common = self.gamestate.common
        face_up = self.gamestate.face_up

        return choice(self.cards)

g = Game(5, ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]))
while g.play() == False:
    print(g.players[0].score, g.players[1].score)