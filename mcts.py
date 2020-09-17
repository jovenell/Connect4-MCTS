from node import Node
from copy import deepcopy
import time
import random

class MCTS:
    def __init__(self, game):
        self.root = Node(game)

    def main(self):
        winning_moves = self.get_winning_moves(self.root)
        if len(winning_moves) > 0:
            return winning_moves[0]
        else:
            opponent_winning_moves = self.get_opponent_winning_moves(self.root)

            if len(opponent_winning_moves) > 0:
                return opponent_winning_moves[0]

        start = time.time()

        while time.time() - start < 20:
            self.simulate(self.root)
        
        return self.best_child(self.root).move_column

    def simulate(self, node):
        while node.game.finished == False:
            if len(node.children) == 0:
                moves = self.get_possible_moves(node)

                for i in moves:
                    game_copy = deepcopy(node.game)

                    node.children.append(Node(game_copy, i, node))

                    node.children[-1].game.place_piece(i)
                    node.children[-1].game.check_if_finished()
                    node.children[-1].game.turn *= -1

            traversed_all_children = True
            for i in node.children:
                if i.num_simulations == 0:
                    traversed_all_children = False
                    break

            if traversed_all_children:
                action = node.children[0]

                for i in node.children:
                    if i.ucb > action.ucb:
                        action = i
            else:
                for i in node.children:
                    if i.num_simulations == 0:
                        action = i
                        break
            node = action

            node.game.check_if_finished()
        
        if self.root.game.turn == node.game.winner:
            self.backpropagate(node, 1)
        elif self.root.game.turn * -1 == node.game.winner:
            self.backpropagate(node, -1)
        elif node.game.winner == 0:
            self.backpropagate(node, 0)

    def backpropagate(self, node, result):
        if node == self.root:
            self.root.num_simulations += 1
            return

        node.update_results(result)
        
        self.backpropagate(node.parent, result)

    def best_child(self, node):
        losing_moves = self.get_losing_moves(node)
        best = None

        for i in self.root.children:
            if i.move_column not in losing_moves:
                best = i
                break

        for i in self.root.children:
            if i.ucb > best.ucb and i.move_column not in losing_moves:
                best = i

        if best == None:
            return self.root.children[0]
        else:
            return best


    def get_possible_moves(self, node):
        moves = []
        
        for i in range(7):
            if node.game.board[0][i] == 0:
                moves.append(i)
        return moves

    def get_winning_moves(self, node):
        moves = []
        
        for i in range(7):
            game_copy = deepcopy(node.game)
            game_copy.place_piece(i)
            game_copy.check_if_finished()

            if game_copy.finished:
                moves.append(i)

        return moves

    def get_opponent_winning_moves(self, node):
        moves = []

        for i in range(7):
            game_copy = deepcopy(node.game)
            game_copy.turn *= -1
            game_copy.place_piece(i)
            game_copy.check_if_finished()

            if game_copy.finished:
                moves.append(i)

        return moves

    def get_losing_moves(self, node):
        moves = []
        
        for i in range(7):
            for j in range(7):
                game_copy = deepcopy(node.game)
                game_copy.place_piece(i)
                game_copy.turn *= -1
                game_copy.place_piece(j)
                game_copy.check_if_finished()

                if game_copy.finished:
                    moves.append(i)

        return moves
