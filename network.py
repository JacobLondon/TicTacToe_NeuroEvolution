import numpy as np
import random
import pickle
from itertools import combinations

class Layer(object):
    
    def __init__(self, num_in, num_out):
        self.weights = np.zeros((num_out, num_in))
        self.bias = np.zeros(num_out)
        
    def forward(self, x):
        x = np.matmul(self.weights, x)
        x = self.bias + x
        x = 1 / (1 + np.exp(-x))
        return x

    def mutate(self, mutation_rate=0.5, mutation_amt=0.1):
        
        for row in range(self.weights.shape[0]):
            # only mutate sometimes
            if random.uniform(0.0, 1.0) <= mutation_rate:
                for col in range(self.weights.shape[1]):
                    
                    self.weights[row, col] += mutation_amt * random.uniform(-1, 1)
        
        for i in range(self.bias.shape[0]):
            self.bias[i] += mutation_amt * random.uniform(-1,1)


class Agent(object):
    
    def __init__(self):
        self.layers = self.build_layers()
        self.fitness = 1
        self.games_won = 0
        self.age = 0

    def __str__(self):
        return "f= " + str(self.fitness)

    def build_layers(self):
        # 9 36 18 9
        l_sizes = [9, 27, 18, 9]
        layers = []
        for value in range(len(l_sizes) - 1):
            layers.append(Layer(l_sizes[value], l_sizes[value + 1]))
        return layers

    def forward(self, x):
        x = x.reshape(-1)
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def pick_move(self, x):
        x = self.forward(x)
        return int(np.argmax(x))

    def mutate(self, mutation_rate=0.5, mutation_amt=0.1):
        for layer in self.layers:
            layer.mutate(mutation_rate=mutation_rate, mutation_amt=mutation_amt)

    def save(self, location):
        pickle.dump(self, open(location, 'wb'))

    @staticmethod
    def load(location):
        return pickle.load(open(location, 'rb'))