import random
import numpy as np
from route import Heuristics, Graph_Collect
from Constants import *
import copy


def initial_population(G, H, source, target):
    population = []
    individual = Heuristics._best_first_search(G, H, source, target, VEHICLE_MASS)
    for i in range(0, AMOUNT_INDIVIDUALS):
        population.append(individual)
    return population


def fitness_individual(G, H, individual):
    total_work_individual = Graph_Collect.sum_costs_route(G, H, individual, VEHICLE_MASS)
    return total_work_individual


def fitness_population(G, H, population):
    len_pop = len(population)
    fitness_population = []

    for i in range(len_pop):
        aptitude = fitness_individual(G, H, population[i])
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
    sumAptitude = 0

    # sum of all values of fitness
    for i in range(len(fitness_pop)):
        sumAptitude += fitness_pop[i]

    # list with the probability value
    # about each individual to be selected
    probabilities = {}

    for i in range(len(fitness_pop)):
        probability = fitness_pop[i] / sumAptitude
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
    for i in range(len(population)-1):
        if population[i] != population[i+1]:
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
    index_node_2 = 0

    node_1 = random.choice(individual_copy_1)
    index_node_1 = individual.index(node_1)

    flag = True
    while flag is True:
        node_2 = random.choice(individual_copy_1)
        index_node_2 = individual.index(node_2)
        if node_1 != node_2:
            flag = False

    new_individual[index_node_1] = individual[index_node_2]
    new_individual[index_node_2] = individual[index_node_1]

    return new_individual


def verify_node_repeat(individual):
    repeated = []
    for i in range(len(individual)):
        if individual.count(individual[i]) > 1:
            repeated.append(individual[i])
    return repeated


def verifying_node_missing(individual, nodes):
    missing = []
    for i in nodes:
        if i not in list(individual):
            missing.append(i)
    return missing


def correct_individual(individual, source, target, nodes):

    # if the last chromosome is not the destination of the route
    # print("to correct:", individual)
    if individual[-1] != target:
        if individual.index(target) is None:
            if source == target:
                individual.insert(0, source)
                individual.append(target)
            else:
                individual.insert(0, source)

        elif source == target:
            individual.append(target)

        else:
            # remove from the current position
            individual.remove(target)
            # insert the target on the final of individual
            individual.append(target)
    # print("apos corrigir final", individual)

    # if the first chromosome is not the source of the route
    if individual[0] != source:
        if individual.index(source) is None:
            if source == target:
                individual.insert(0, source)
                individual.append(target)
            else:
                individual.insert(0, source)
        elif source == target:
            individual.insert(0, source)
        else:
            # remove from the current position
            individual.remove(source)
            # insert the target on the final of individual
            individual.insert(0, source)
    # print("apos corrigir inicio", individual)

    # verify and remove repeated nodes side by side
    n = 0
    while n < len(individual) - 1:
        if individual[n] == individual[n + 1]:
            individual.remove(individual[n])
        n += 1
    # print("apos remover repetidos lado a lado", individual)

    # remove repeated nodes
    test_individual = individual.copy()
    test_individual.remove(test_individual[0])
    test_individual.remove(test_individual[-1])
    repeated = verify_node_repeat(test_individual)
    while len(repeated) > 0:
        new_individual = []
        indices = [i for i, x in enumerate(test_individual) if x == repeated[0]]
        for j in range(len(test_individual)):
            if indices[0] <= j < indices[-1]:
                pass
            else:
                new_individual.append(test_individual[j])
        test_individual = new_individual
        repeated = verify_node_repeat(test_individual)
    test_individual.insert(0, source)
    test_individual.append(target)
    individual = test_individual
    # print("apos remover repetidos", individual)

    # if a node is not in the individual
    missing = verifying_node_missing(individual, nodes)
    if len(missing) > 0:
        for i in missing[::-1]:
            individual.insert(1, i)
    # print("apos ver missing", individual)

    return individual


def crossover(individual1, individual2, source, target, nodes):

    individual_1 = individual1.copy()
    individual_2 = individual2.copy()

    if len(individual_1) > 2 and len(individual_2) > 2:
        del individual_1[-1]
        individual_1.remove(individual_1[0])
        del individual_2[-1]
        individual_2.remove(individual_2[0])
        #print("apos remover inicio e fim", individual_1, individual_2)

        node_1 = random.choice(individual_1)
        # print("node 1", node_1)
        index_1 = individual1.index(node_1)
        node_2 = random.choice(individual_2)
        index_2 = individual2.index(node_2)
        # print("node 2", node_2)

        child_1_1 = individual_1[0:index_1]
        # print("child_1_1", child_1_1)
        child_1_2 = individual_1[index_1:]
        # print("child_1_2", child_1_2)

        child_2_1 = individual_2[0:index_2]
        # print("child_2_1", child_2_1)
        child_2_2 = individual_2[index_2:]
        # print("child_2_2", child_2_2)

        child1 = child_1_2 + child_1_1
        child2 = child_2_2 + child_2_1

        child1.insert(0, source)
        child1.append(target)
        child2.insert(0, source)
        child2.append(target)

        # print("antes da correcao (1)", child1)
        # print("antes da correcao (2)", child2)

        child1 = correct_individual(child1, source, target, nodes)
        child2 = correct_individual(child2, source, target, nodes)

        return child1, child2


def best_individual(population, fitness_pop):

    min_fitness = fitness_pop[0]
    index_min = 0

    for i in range(len(fitness_pop)):
        if fitness_pop[i] < min_fitness:
            min_fitness = fitness_pop[i]
            index_min = i

    print("The best fitness is:", min_fitness, population[index_min])
    return population[index_min]


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
        # print("crossover apos correcao", child1, child2)

    # best individual
    individual_best = best_individual(copy_population, fitness_pop)
    generation.append(individual_best)

    new_generation = []
    for i in generation:
        individual_correct = correct_individual(i, source, target, nodes)
        new_generation.append(individual_correct)

    return new_generation


def GA(G, H, source, target, nodes):

    population_initial = initial_population(G, H, source, target)
    population = population_initial.copy()

    n_generation = 0
    criterion = True
    while criterion is True:
        fitness = fitness_population(G, H, population)
        population = next_generation(population, fitness, source, target, nodes)
        # print("Population", population)
        # print("Fitness", fitness)
        if n_generation == LIMIT_ITERATION:
            criterion = False
        n_generation += 1

    print("initial pop", population_initial)
    print("Fitness last gen", fitness)

    best = best_individual(population, fitness)
    index_best = population.index(best)
    print("The best route is:", best, fitness[index_best])
    return best