import random
import numpy as np
from route import Heuristics, Graph_Collect
from Constants import *
import copy


def initial_population(G, H, source, target):
    population = []
    individual_1 = Heuristics.nearest_neighbor(G, H, source, target, VEHICLE_MASS)
    individual_2 = Heuristics.closest_insertion(G, H, source, target)
    possibilities = list(H.nodes)
    if source != target:
        possibilities.remove(source)
        possibilities.remove(target)
    else:
        possibilities.remove(source)
    population.append(individual_1)
    population.append(individual_2)
    for i in range(AMOUNT_INDIVIDUALS-2):
        population.append(create_individual(possibilities, source, target))
    return population


def create_individual(possibilities, source, target):
    individual = [source]
    while len(individual) < len(possibilities):
        nodes = set(possibilities) - set(individual)
        individual.append(random.choice(list(nodes)))
    individual.append(target)
    return individual


def fitness_individual(G, H, individual, impedance):
    total_work_individual, _ = Graph_Collect.sum_costs_route(G, H, individual, VEHICLE_MASS, impedance)
    return total_work_individual


def fitness_population(G, H, population, impedance):
    len_pop = len(population)
    fitness_population = []

    for i in range(len_pop):
        aptitude = fitness_individual(G, H, population[i], impedance)
        fitness_population.append(aptitude)

    return fitness_population


def windowing(fitness_pop):
    # decreases all fitness values by the minimum value
    new_fitness = []
    min1 = min(fitness_pop)

    for i in range(len(fitness_pop)):
        value = fitness_pop[i] - min1
        new_fitness.append(value)
    return new_fitness


def exponential_transformation(fitness_pop):
    # exponential transformation of fitness
    new_fitness = []
    for i in range(len(fitness_pop)):
        value = fitness_pop[i] + 1
        new_fitness_value = value ** (1 / 2)
        new_fitness.append(new_fitness_value)
    return new_fitness


def linear_normalization(fitness_pop):
    # linear normalization
    idSort = np.argsort(fitness_pop)
    N = 20  # increment
    i = 0

    for idValue in idSort:
        fitness_pop[i] = (idValue) * N + 1
        i = i + 1
    return fitness_pop


def roulette(randomNumber, population, fitness_pop):
    selected = []
    sum_aptitude = 0

    # sum of all values of fitness
    sum_aptitude = sum(fitness_pop)

    # list with the probability value
    # about each individual to be selected
    probabilities = {}

    for i in range(len(fitness_pop)):
        probability = fitness_pop[i] / sum_aptitude
        probabilities.update([(i, probability)])

    # sort the probability values in ascending order
    probabilities = dict(sorted(probabilities.items(), key=lambda item: item[1]))

    # verify the interval of random number
    # sum_probabilities == 1 in the end of the loop
    sum_probabilities = 0
    probabilities_values = list(probabilities.values())
    probabilities_keys = list(probabilities.keys())
    for j in range(len(probabilities.values())):
        sum_probabilities += probabilities_values[j]
        if float(randomNumber) <= sum_probabilities:
            # probabilities_keys[j] == index of individual in
            # population list
            return population[probabilities_keys[j]]


def alike_individuals(population):
    for i in range(len(population) - 1):
        if population[i] != population[i + 1]:
            return False
    return True


def select_individual(amount_individuals, population, fitness_pop):
    # select parents for crossover and select individual for mutation

    n_selecteds = 0
    selecteds = []

    # verify if the individual has already been selected
    individual_already_selected = False

    # about quantity of individuals must be selected
    while n_selecteds != amount_individuals:

        # return the next random floating point number in the range [0.0, 1.0)
        randomNumber = random.random()
        selected = roulette(randomNumber, population, fitness_pop)  # select one individual by roulette

        # if there is any selected individual on the list, it is necessary
        # to verify if the current selected individual
        # has been selected before
        if len(selecteds) > 0:
            for j in range(len(selecteds)):

                # if the individual selected has already been stored
                if selecteds[j] == selected:

                    # if all individual is the same,
                    # the loop must be finished with any individual
                    if alike_individuals(population) is True:
                        individual_already_selected = False
                    else:
                        individual_already_selected = True
                else:
                    individual_already_selected = False

            # if the individual not selected yet
            if individual_already_selected is False:
                selecteds.append(selected)
        else:
            selecteds.append(selected)
        n_selecteds = len(selecteds)

    return selecteds


def mutation(individual):
    # Change 2 chromosome positions
    # Ex: [1 5 3 4 7] -> [1 4 3 5 7]

    individual_copy_1 = individual.copy()
    new_individual = individual.copy()
    individual_copy_1.remove(individual[-1])
    individual_copy_1.remove(individual[0])

    node_1 = random.choice(individual_copy_1)
    index_node_1 = individual.index(node_1)

    node_2 = random.choice(individual_copy_1)
    index_node_2 = individual.index(node_2)

    new_individual[index_node_1] = individual[index_node_2]
    new_individual[index_node_2] = individual[index_node_1]

    return new_individual


def verify_node_repeat(individual):
    repeated = [allele for allele in individual if individual.count(allele) > 1]

    return repeated


def verifying_node_missing(individual, nodes):
    missing = [node for node in nodes if individual.count(node) < 1]

    return missing


def correct_individual(individual, source, target, nodes):
    # if the last chromosome is not the destination of the route
    # print("to correct:", individual)
    if individual[-1] != target:
        individual.append(target)

    # if the first chromosome is not the source of the route
    if individual[0] != source:
        individual.insert(0, source)

    # remove repeated nodes
    individual.remove(individual[0])
    individual.remove(individual[-1])

    while target in individual: individual.remove(target)
    while source in individual: individual.remove(target)

    repeated = verify_node_repeat(individual)
    while len(repeated) > 0:
        individual.remove(repeated[0])
        repeated = verify_node_repeat(individual)

    individual.insert(0, source)
    individual.append(target)

    # if a node is not in the individual
    missing = verifying_node_missing(individual, nodes)
    for i in missing[::-1]:
        individual.insert(1, i)

    return individual


def crossover(individual1, individual2, source, target, nodes):
    individual_1 = individual1.copy()
    individual_2 = individual2.copy()

    if len(individual_1) > 2 and len(individual_2) > 2:
        del individual_1[-1]
        individual_1.remove(individual_1[0])
        del individual_2[-1]
        individual_2.remove(individual_2[0])

        node_1 = random.choice(individual_1)
        index_1 = individual1.index(node_1)
        node_2 = random.choice(individual_2)
        index_2 = individual2.index(node_2)

        child_1_1 = individual_1[0:index_1]
        child_1_2 = individual_1[index_1:]

        child_2_1 = individual_2[0:index_2]
        child_2_2 = individual_2[index_2:]

        child1 = child_1_2 + child_1_1
        child2 = child_2_2 + child_2_1

        child1.insert(0, source)
        child1.append(target)
        child2.insert(0, source)
        child2.append(target)

        return child1, child2


def best_individual(population, fitness_pop):

    minimum_fitness = min(fitness_pop)
    index_minimum = fitness_pop.index(minimum_fitness)
    individual_best = population[index_minimum]

    return individual_best


def next_generation(population, fitness_pop, source, target, nodes):
    copy_population = copy.deepcopy(population)
    points = []
    generation = []

    # mutation
    amount_individuals = int((MUTATION_PERCENTAGE / 100) * AMOUNT_INDIVIDUALS)
    selected = select_individual(amount_individuals, copy_population, fitness_pop)
    for a in range(amount_individuals):
        mutated_individual = mutation(selected[a])
        generation.append(mutated_individual)

    # crossover
    amount_individuals = int((CROSSOVER_PERCENTAGE / 100) * AMOUNT_INDIVIDUALS)
    selected = select_individual(amount_individuals, copy_population, fitness_pop)
    for a in range(0, amount_individuals, 2):
        child1, child2 = crossover(selected[a], selected[a + 1], source, target, nodes)
        generation.append(child1)
        generation.append(child2)

    # best individual
    individual_best = best_individual(copy_population, fitness_pop)
    generation.append(individual_best)

    return generation


def GA(G, H, source, target, nodes, impedance):
#def GA(G, H, source, target, nodes, impedance=IMPEDANCE):
    population_initial = initial_population(G, H, source, target)
    population = population_initial.copy()
    fitness = []

    n_generation = 0
    criterion = True
    bests = []
    while criterion is True:
        fitness = fitness_population(G, H, population, impedance)
        fitness = exponential_transformation(fitness)
        population = next_generation(population, fitness, source, target, nodes)
        bests.append(population[-1])
        if n_generation == LIMIT_ITERATION:
            criterion = False
        elif len(bests) > 6:
            if bests[len(bests)-1] == bests[len(bests)-4]:
                criterion = False
        n_generation += 1

    # print("initial pop", population_initial)
    # print("n_generation", n_generation)
    # print("Fitness last gen", fitness)

    best = best_individual(population, fitness)
    index_best = population.index(best)
    cost = fitness[index_best]

    return best
