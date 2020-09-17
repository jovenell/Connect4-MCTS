from mcts import MCTS

class Game:
    def __init__(self, turn=1, winner=0, finished=False, board=[[0 for i in range(7)] for i in range(6)]):
        self.turn = turn
        self.winner = winner
        self.finished = finished
        self.board = board

    def __copy__(self):
        return type(self)(self.turn, self.winner, self.finished, self.board)

    def run(self):
        while self.finished == False:
            if self.turn == 1:
                self.request_input()
            elif self.turn == -1:
                mcts = MCTS(self)
                move = mcts.main()
                self.place_piece(move)

            self.print_board()
            self.check_if_finished()
            self.turn *= -1

    def print_board(self):
        newBoard = []
        for i in self.board:
            newBoard.append([])
            for j in i:
                if j == -1:
                    newBoard[-1].append('O')
                elif j == 0:
                    newBoard[-1].append('-')
                elif j == 1:
                    newBoard[-1].append('X')

        print()
        print('-----------------------------')
        for i in newBoard:
            print('| ' + ''.join([str(j) + ' | ' for j in i]))
        print('-----------------------------')
        print()

    def place_piece(self, column):
        for i in range(1, len(self.board) + 1):
            if self.board[-i][column] == 0:
                self.board[-i][column] = self.turn
                return True
        
        return False

    def request_input(self):
        print('')
        print('--------------------------')
        print('Please enter a digit between 0 and 6 inclusive')

        column = -1

        while column < 0 or column > 6:
            requestedColumn = input()
            try:
                column = int(requestedColumn)

                if not self.place_piece(column):
                    print('')
                    print('Invalid entry, column is full')
                    print('Please enter a digit between 0 and 6 inclusive')

                    column = -1
            except:
                print('')
                print('Invalid entry')
                print('Please enter a digit between 0 and 6 inclusive')

    def check_if_finished(self):
        for i in self.board:
            for j in range(4):
                if sum(i[j:j+4]) == 4:
                    self.finished = True
                    self.winner = 1
                    return
                elif sum(i[j:j+4]) == -4:
                    self.finished = True
                    self.winner = -1
                    return

        for i in range(len(self.board[0])):
            for j in range(3):
                if sum([self.board[j][i], self.board[j + 1][i], self.board[j + 2][i], self.board[j + 3][i]]) == 4:
                    self.finished = True
                    self.winner = 1
                    return
                elif sum([self.board[j][i], self.board[j + 1][i], self.board[j + 2][i], self.board[j + 3][i]]) == -4:
                    self.finished = True
                    self.winner = -1
                    return

        for i in range(len(self.board) - 3):
            for j in range(len(self.board[0]) - 3):
                if sum([self.board[i][j], self.board[i + 1][j + 1], self.board[i + 2][j + 2], self.board[i + 3][j + 3]]) == 4:
                    self.finished = True
                    self.winner = 1
                    return
                elif sum([self.board[-(i + 1)][j], self.board[-(i + 1) - 1][j + 1], self.board[-(i + 1) - 2][j + 2], self.board[-(i + 1) - 3][j + 3]]) == 4:
                    self.finished = True
                    self.winner = 1
                    return
                elif sum([self.board[i][j], self.board[i + 1][j + 1], self.board[i + 2][j + 2], self.board[i + 3][j + 3]]) == -4:
                    self.finished = True
                    self.winner = -1
                    return
                elif sum([self.board[-(i + 1)][j], self.board[-(i + 1) - 1][j + 1], self.board[-(i + 1) - 2][j + 2], self.board[-(i + 1) - 3][j + 3]]) == -4:
                    self.finished = True
                    self.winner = -1
                    return

        for i in self.board:
            for j in i:
                if j == 0:
                    return

        self.finished = True
        self.winner = 0
        return

