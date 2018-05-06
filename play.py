from tictactoe import TicTacToe
from network import Agent
from player import Player
import pickle

# player against ai
def play(player0, player1):
    
    game = TicTacToe(printing=True)
    game.print_board()

    # play game
    while game.winner == -1:
        if game.player == 0:
            winner = game.play(player0.get_input())
        else:
            winner = game.play(player1.get_input(board=game.board))
    return winner

if __name__ == '__main__':
    agent = input('Enter the name of the file to play:\n')
    agent = Agent.load(f'players/{agent}')
    player0 = Player()
    player1 = Player(agent=agent)

    replay = 'y'
    while replay == 'y':
        print(play(player0, player1), 'won the game.')
        replay = input('Play again?\ny/n\n')