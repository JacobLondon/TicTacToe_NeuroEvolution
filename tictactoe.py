import numpy as np
import copy

class TicTacToe(object):

    def __init__(self, printing=True):

        self.printing = printing
        self.board = np.zeros((3,3)) - 1
        self.player = 0
        self.turn_number = 0
        self.winner = -1
        self.moves = []
        self.location = {1:(0,0), 2:(0,1), 3:(0,2), 4:(1,0), 5:(1,1), 6:(1,2), 7:(2,0), 8:(2,1), 9:(2,2)}

    def place(self, pos):
        pos = int(pos)

        # the dictionary of the position at pos x,y
        if self.board[self.location[pos][0]][self.location[pos][1]] == -1:
            self.board[self.location[pos][0]][self.location[pos][1]] = copy.deepcopy(self.player)
            self.switch()
        # the position has been placed before
        else:
            if self.printing:
                print('Location',self.location[pos][0], ',', self.location[pos][1],'is full.')
            return -1


    def switch(self):
        self.turn_number += 1
        self.player = self.turn_number % 2


    # determine fitness based on number of moves?
    def check_win(self):
        player0_moves = self.moves[0::2]
        player1_moves = self.moves[1::2]

        # player 0 won
        if self.win_positions(player0_moves):
            return self.player

        # player 1 won
        elif self.win_positions(player1_moves):
            return self.player

        # draw
        elif self.turn_number >= 9:
            return -2

        # game continue
        else:
            return -1

                
    def win_positions(self, move_list):
        return set([1,2,3]).issubset(set(move_list)) or \
            set([4,5,6]).issubset(set(move_list)) or \
            set([7,8,9]).issubset(set(move_list)) or \
            set([1,4,7]).issubset(set(move_list)) or \
            set([2,5,8]).issubset(set(move_list)) or \
            set([3,6,9]).issubset(set(move_list)) or \
            set([1,5,9]).issubset(set(move_list)) or \
            set([3,5,7]).issubset(set(move_list))


    def print_board(self):
        
        output = {-1:'_', 0:'O', 1:'X'}

        # board
        for row in self.board:
            print('\n')
            for value in row:
                print(output[value], end='')
        print('\n')

        # user placement key
        for item in range(len(self.location)):
            print(item+1, ' ', end='')
            if (item+1) % 3 == 0:
                print('\n')
        print('\n')
        

    def play(self, player_move):
        
        # place and record moves
        pos = self.place(player_move)

        # if move already occured
        if pos == -1:
            
            # ai 0 tried to replay
            if self.player == 0:
                self.winner = -3
                return self.winner
            # ai 1 tried to replay
            else:
                self.winner = -4
                return self.winner
        else:
            self.moves.append(int(player_move))

        # check for winner
        if not self.check_win() == -1:
            self.switch() # correct for switching
            self.winner = self.check_win()
            return self.winner
        if self.printing:
            self.print_board()

        # no winner this round
        return -1

# play game with 2 people
if __name__ == '__main__':

    player_game = TicTacToe(printing=True)
    player_game.print_board()

    while player_game.winner == -1:
        if player_game.player == 0:
            winner = player_game.play(input('p0 input: '))
        else:
            winner = player_game.play(input('p1 input: '))
    print('winner is ', winner)
