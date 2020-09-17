import numpy as np
import math

class Node():
    def __init__(self, game, move_column=None, parent=None):
        self.game = game
        self.move_column = move_column
        self.parent = parent
        self.children = []
        self.num_simulations = 0
        self.num_winning_simulations = 0
        self.num_tying_simulations = 0
        self.num_losing_simulations = 0
        self.ucb = 0

    def update_results(self, result):
        self.num_simulations += 1
        
        if result == 1:
            self.num_winning_simulations += 1
        elif result == 0:
            self.num_tying_simulations += 1
        elif result == -1:
            self.num_losing_simulations += 1

        value_of_node = ((self.num_winning_simulations) + (self.num_tying_simulations * 0.5) - (self.num_losing_simulations))
        constant = 2

        self.ucb = value_of_node + constant * math.sqrt(math.log(self.parent.num_simulations + 1) / self.num_simulations)