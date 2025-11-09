import numpy as np
from random import choice

def playerChoice(max_player, min_player, central_cards, face_up_card):
    raise NotImplementedError

def minimax(depth, maxDepth, isMax=False):
    """
    Idea:

    At each depth, run minimax TWICE: once for player1, once for player2, each using their own knowledge
    (neither knows what the other picked until round is over)

    When player1 makes a move, the resulting score of a move is the average score of the result of the move, given all moves player2 could make
    -> Maybe think about considering this equal weighting, then using that to calculate the best score, weighting move based on which was best opponent move for that stage.
    
    Otherwise regular minimax (though maybe not exactly minimax? since this is a simulataneous game... idk what the algorithm would
    be called in this case, just a tree traversal I suppose)
    """
    raise NotImplementedError