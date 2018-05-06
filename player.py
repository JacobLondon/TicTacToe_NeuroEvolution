from network import Agent

class Player(object):
    
    def __init__(self, agent=None):
        self.agent = agent

    
    def get_input(self, board=None):
        if self.agent == None:
            return input('\nEnter move: ')
        else:
            # add 1 for the 1-9 selection
            return self.agent.pick_move(board) + 1

