from network import Layer, Agent
from tictactoe import TicTacToe
from player import Player
from itertools import combinations
from operator import attrgetter
import os, copy, tqdm, random, pickle, numpy as np
import matplotlib
import matplotlib.pyplot as plt

population = 35            # number of agents
generations = 650        # number of generations

mutation_rate = 0.9        # agents affected by mutations per generation
mutation_decrease_rate = 1
mutation_amt = 0.5         # amount mutated

percent_selection = 0.15   # amount to live to next generation
exit_fitness = -1          # alg will stop after worst surpasses this fitness
max_age = 30
new_population = []        # put best in a list and get a new better population

def init_agents(population):
    return [Agent() for _ in range(population)]

def genetic_alg():
    global mutation_rate, new_population
    agents = init_agents(population)
    best = None
    average = 0
    maximum = 0 # the highest fitness point that occured
    fig, ax = plt.subplots()

    # life cycle for each generation
    for generation in tqdm.tqdm(range(generations)):
        
        # check if the new population is ready
        if len(new_population) == population:
            agents = copy.deepcopy(new_population)
            new_population = []

        # find and show best per generation
        agents = fitness(agents)
        best = max(agents, key=attrgetter('fitness'))
        worst = min(agents, key=attrgetter('fitness'))
        for agent in agents:
            average += agent.fitness
        average /= len(agents)
        ax.plot(generation, best.fitness, 'co')
        ax.plot(generation, best.games_won, 'ro')
        #ax.plot(generation, mutation_rate*100,'bo')
        ax.plot(generation, average, 'go')
        ax.plot(generation, worst.fitness, 'yo')

        # decrease the mutation rate over time
        if best.fitness > maximum:
            mutation_rate *= mutation_decrease_rate
            maximum = copy.copy(best.fitness)
        if not exit_fitness == -1 and worst.fitness > exit_fitness:
            break

        agents = selection(agents)
        agents = crossover(agents) # crossover and mutation
    
    print(best)
    plt.title('Performance vs Generations')
    plt.show()
    return fitness(agents)

def fitness(agents):
    unique_indexes = combinations(range(len(agents)), 2)
    
    # each unique combination of ai's against each other
    for index_tuple in unique_indexes:
        
        game = TicTacToe(printing=False)

        # make two players with each unique
        if index_tuple[0] == index_tuple[1]:
            continue
        player0 = Player(agent=agents[index_tuple[0]])
        player1 = Player(agent=agents[index_tuple[1]])
        in_board = game.board.reshape(-1)

        # play game
        while game.winner == -1:
            if game.player == 0:
                
                winner = game.play(player0.get_input(board=in_board))
            else:
                winner = game.play(player1.get_input(board=in_board))
        
        # ai 0 won
        if winner == 0:
            agents[index_tuple[0]].fitness += copy.deepcopy(game.turn_number)
            agents[index_tuple[0]].games_won += 1
            agents[index_tuple[1]].fitness -= 1

        # ai 1 won
        elif winner == 1:
            agents[index_tuple[1]].fitness += copy.deepcopy(game.turn_number)
            agents[index_tuple[1]].games_won += 1
            agents[index_tuple[0]].fitness -= 1

        # draw
        elif winner == -2:
            agents[index_tuple[0]].fitness += 6
            agents[index_tuple[1]].fitness += 6

        # ai 0 tried to replay
        elif winner == -3:
            agents[index_tuple[0]].fitness -= 4 + copy.deepcopy(9-game.turn_number) * 2

        # ai 1 tried to replay
        elif winner == -4:
            agents[index_tuple[1]].fitness -= 4 + copy.deepcopy(9-game.turn_number) * 2

    return agents

# get best agents and remove old agents
def selection(agents):
    global new_population
    for agent in agents:
        agent.age += 1

    # sort list from high to low, keep the top percent_selection
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    agents = agents[:int(percent_selection * len(agents))]

    # put best into a new list
    if agents[0].age >= max_age:
        new_population.append(copy.deepcopy(agents[0]))
        new_population[-1].fitness = 0
        new_population[-1].age = 0
        new_population[-1].games_won = 0

    return agents

# one point crossover
def crossover(agents):
    offspring = []

    # 2 children per iteration
    for _ in range(int((population - len(agents)) / 2)):
        
        # Note: this may select the same parent twice!
        parent1 = random.choice(agents)
        parent2 = random.choice(agents)
        child1 = Agent()
        child2 = Agent()
        
        # look at each row of each layer
        for layer in range(len(parent1.layers)):
            for row in range(len(parent1.layers[layer].weights)):
                
                # assign shorter vars
                parent1_row = parent1.layers[layer].weights[row]
                parent2_row = parent2.layers[layer].weights[row]

                # find a location to split the array
                split = random.randint(0, len(parent1_row))

                # make two children based off of each parent split combination
                child1.layers[layer].weights[row] = copy.deepcopy(np.append(parent1_row[0:split], parent2_row[split:len(parent1_row)]))
                child2.layers[layer].weights[row] = copy.deepcopy(np.append(parent2_row[0:split], parent1_row[split:len(parent1_row)]))

        # put the children into a list
        offspring.append(child1)
        offspring.append(child2)

    # put offspring list onto the end of all agents (the population)
    agents.extend(mutation(offspring))

    return agents

def mutation(offspring):
    for agent in offspring:
        agent.mutate(mutation_rate=mutation_rate, mutation_amt=mutation_amt)
    return offspring

# player against ai
def play(player0, player1):
    
    game = TicTacToe(printing=True)
    game.print_board()

    in_board = game.board.reshape(-1)

    # play game
    while game.winner == -1:
        if game.player == 0:
            winner = game.play(player0.get_input())
        else:
            winner = game.play(player1.get_input(board=in_board))
    return winner

if __name__ == '__main__':
    last_gen = genetic_alg()
    best = max(last_gen, key=attrgetter('fitness'))
    
    count = 0
    for agent in last_gen:
        print(agent, end='\t')
        if count % 5 == 0:
            print('\n')
        count += 1

    player0, player1 = Player(agent=None), Player(agent=best)
    print(play(player0, player1),'won the game.')
    
    # save the best to file
    print('Save to file?\n')
    if input('y/n\n') == 'y':
        if not os.path.exists("players"):
            os.mkdir("players")
        name = input('Enter the name of the agent:\n')
        best.save(f'players/{name}')
    
