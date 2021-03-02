import random
from random import randint
import numpy as np
import copy
import csv
import ConsumptionModel as cM
import math
import Map
import json
import bfs
import dfs
import astar
import mainSumo


class GA:

    def __init__(self, csvFile, nodes, edges, inicio, destino, nIndividuals, limitGen, MapObject, code):
        self.csv = csvFile
        self.matrix = []
        self.n_individuals = nIndividuals  # 7
        self.population = []
        self.fitness = []
        self.nodes = nodes
        self.edges = edges
        self.edgesV = {}  # edges vizinhas
        self.limit = limitGen  # 20 # generation limit
        self.criterion = False
        self.bestFitness = 0
        self.fitnessDesired = 10000
        self.inicio = inicio
        self.destino = destino
        self.map = MapObject  # Map.Map('SUMO/map')
        self.map.run()
        self.code = code
        self.bfs = bfs.Graph()
        self.dfs = dfs.DFS()

    def setInitialPop(self):
        for i in range(0, self.n_individuals):
            # individual = self.h_astar(self.inicio,self.destino)
            individual = self.h_dfs(self.inicio, self.destino)
            self.population.append(individual)

    def h_bfs(self, inicio, objetivo):
        rota = self.bfs.run(inicio, objetivo, self.nodes, self.edges)
        return rota

    def h_dfs(self, inicio, objetivo):
        rota = self.dfs.run(inicio, objetivo, self.edgesV)
        return rota

    def h_astar(self, inicio, objetivo):
        rota = astar.main(self.edgesV, self.nodes, inicio, objetivo, self.map)
        return rota

    def setMatrix(self):
        with open(self.csv + '.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            matrix = []
            for row in spamreader:
                matrix.append(row)
        self.matrix = matrix

    def getMatrix(self):
        return self.matrix

    def cfitness(self, vectorIndividual):
        edgesIndividual = self.map.getListEdges(vectorIndividual)
        consumption = mainSumo.main(edgesIndividual, 'GA', self.code)
        return consumption

    def setFitnessPopulation(self, population):
        len_pop = len(population)
        fitness = []
        sum1 = 0

        for i in range(len_pop):
            aptitude = self.cfitness(population[i])
            fitness.append(aptitude)

        return fitness

    def getFitnessPopulation(self):
        return self.fitness

    def windowing(self):
        # decreases all aptitude values by the minimum value        
        newList = []
        min1 = min(self.fitness)
        for i in range(len(self.fitness)):
            value = self.fitness[i] - min1
            newList.append(value)
        return newList

    def expTransformation(self):
        # exponential transformation
        newList = []
        for i in range(len(self.fitness)):
            value = self.fitness[i] + 1
            value1 = value ** (1 / 2)
            newList.append(value1)
        return newList

    def linearNormFuction(self):
        # linear normalization
        idSort = np.argsort(self.fitness)
        N = 20  # increment
        i = 0
        for idValue in idSort:
            self.fitness[i] = (idValue) * N + 1
            i = i + 1
        return self.fitness

    def setBestIndividual(self, population):

        fit = self.setFitnessPopulation(population)
        var = fit[0]
        index = 0

        for i in range(len(fit)):
            if fit[i] < var:
                var = fit[i]
                index = i

        self.bestFitness = float(fit[index])
        self.bestIndividual = population[index]

    def getBestIndividual(self):
        return self.bestIndividual

    def roulette(self, randomNumber, population, fitness):

        selected = []
        sumAptitude = 0

        # sum of all valued of fitness
        for i in range(len(fitness)):
            sumAptitude += fitness[i]

        # create a list with the probability value about each individual to be selected
        probabilities = []

        for i in range(len(fitness)):
            probability = fitness[i] / sumAptitude
            probabilities.append(probability)

            # sort in ascending order
        probabilities.sort()

        # verify the interval of random number
        # sum_probabilities == 1 in the end of the loop
        sum_probabilities = 0
        for a in range(len(probabilities)):
            sum_probabilities += probabilities[a]
            if float(randomNumber) <= sum_probabilities:
                return population[a]

    def selectIndiv(self, amount, population, fitness):
        # select parents for crossover and select individual for mutation

        quant = 0
        selecteds = []
        indivAlreadyStored = False  # to verify if the individual has already been stored

        while quant != amount:  # about quantity of individuals must be selected

            randomNumber = random.random()  # return the next random floating point number in the range [0.0, 1.0)
            selected = self.roulette(randomNumber, population, fitness)  # select one individual by roulette

            if len(selecteds) > 0:
                for j in range(len(selecteds)):
                    if selecteds[j] == selected:  # if the individual selected has already been stored
                        if population[0] == population[1] == population[
                            2]:  # == self.population[3]:
                            indivAlreadyStored = False  # if all individual is the same, the loop must be finished with any individual
                        else:
                            indivAlreadyStored = True
                    else:
                        indivAlreadyStored = False
                if indivAlreadyStored == False:
                    selecteds.append(selected)
            else:
                selecteds.append(selected)
            quant = len(selecteds)

        if len(selecteds) > 1:
            return selecteds
        elif len(selecteds) == 1:  # if it is just one individual, it is not returned inside other list
            return selecteds[0]

    def mutation(self, individual, typ):
        indiv1 = individual.copy()
        valid = 0
        falg = False
        options = []
        indices = []

        if typ == 1:
            for i in range(1, len(individual) - 1):
                if self.validateRoute(individual[i - 1],
                                      individual[i + 1]) == True:  # testa se eh possivel remover algum noh
                    valid = i
            if valid != 0:  # se for possivel remover um node
                newIndividual = indiv1.remove(individual[valid])
                return newIndividual
        for i in range(0, len(individual) - 2):  # não precisa substituir o penultimo
            possibilities = self.edgesV.get(individual[i])
            if len(possibilities) > 1:
                options.append(individual[i])
                indices.append(i)
        if len(options) > 0:
            chosen = random.choice(options)
            indice = options.index(chosen)
            indice1 = indices[indice]
            possibilities1 = self.edgesV.get(chosen)
            if individual[indice1 + 1] in possibilities1: possibilities1.remove(
                individual[indice1 + 1])  # possibilities1.remove(individual[indice1 + 1])
            if indice1 > 0 and individual[indice1 - 1] in possibilities1: possibilities1.remove(individual[indice1 - 1])
            if len(possibilities1) > 0:
                newPossib = random.choice(possibilities1)
                newPath = self.h_bfs(newPossib, self.destino)
                # newPath = self.h_astar(newPossib,self.destino)
                if newPath == "error":
                    return individual
                newIndividual = individual[0:indice1 + 1] + newPath
                return newIndividual
        return individual

    def crossover(self, individual1, individual2):

        ind1 = individual1.copy()
        ind2 = individual2.copy()

        if len(ind1) > 2 and len(ind2) > 2:
            ind1.remove(ind1[-1])
            ind1.remove(ind1[0])
            ind2.remove(ind2[-1])
            ind2.remove(ind2[0])

            child1 = []
            child2 = []
            temp1 = []
            temp2 = []

            a = random.choice(ind1)
            index1 = individual1.index(a)
            b = random.choice(ind2)
            index2 = individual2.index(b)

            child1 = individual1[0:index1]
            temp2 = individual1[index1:]

            child2 = individual2[0:index2]
            temp1 = individual2[index2:]

            child1 = child1 + temp1
            child2 = child2 + temp2

            child1 = self.correct(child1)
            child2 = self.correct(child2)

            return child1, child2

    def setEdgesV(self):
        for i in self.nodes:
            self.edgesV.update([(i, {})])
            for j in self.nodes:
                if self.validateRoute(i, j) == True:
                    item = self.edgesV.get(i)
                    item = list(item)
                    item.append(j)
                    self.edgesV.update([(i, item)])

    def setEdgesV1(self):
        for i in self.nodes:
            self.edgesV.update([(i, {})])
            for j in self.nodes:
                if self.validateRoute(i, j) == True:
                    item = self.edgesV.get(i)
                    item = list(item)
                    item.append(j)
                    self.edgesV.update([(i, item)])

    def getEdgesV(self):
        return self.edgesV

    def validatePop(self, population):
        errors = []  # index of wrong individuals
        for i in range(len(population)):
            test = self.validateInd(population[i])
            if test == False:
                errors.append(i)
        return errors

    def validateInd(self, individual):
        flag = True
        repeated = self.setRepeated(individual)
        if len(repeated) > 0:
            flag = False
        else:
            for i in range(len(individual) - 1):
                test = self.validateRoute(individual[i], individual[i + 1])
                if test == False:
                    flag = False
        return flag

    def validateRoute(self, a, b):
        cost = 0

        for i in range(len(self.matrix)):
            if str(self.matrix[i][0]) == str(a):
                initialPoint = i
                for j in range(len(self.matrix[0])):
                    if str(self.matrix[0][j]) == str(b):
                        finalPoint = j
                        cost = self.matrix[initialPoint][finalPoint]
                        if cost == "":
                            return False
                        else:
                            return True

    def correct(self, individual):
        indices = []
        repeated = []
        flag = False
        alell = len(individual) - 1

        ##### se o individuo não vai até o destino
        if individual[-1] != self.destino:
            newPath = self.h_bfs(individual[-1], self.destino)
            # newPath = self.h_astar(individual[-1],self.destino)
            if newPath == "error":
                while alell > 0 and flag == False:
                    newPath = self.h_bfs(individual[alell], self.destino)
                    # newPath = self.h_astar(individual[alell],self.destino)
                    if newPath != "error":
                        individual = individual[:alell] + newPath
                        flag = True
                    alell -= 1
            else:
                individual = individual + newPath[1:]

        ##### se o individuo não começa no inicio
        flag = False
        alell = 1
        if individual[0] != self.inicio:
            newPath = self.h_bfs(self.inicio, individual[0])
            # newPath = self.h_astar(self.inicio,individual[0])
            if newPath == "error":
                while alell < len(individual) - 1 and flag == False:
                    newPath = self.h_bfs(self.inicio, individual[alell])
                    # newPath = self.h_astar(self.inicio,individual[alell])
                    if newPath != "error":
                        individual = newPath + individual[alell:]
                        flag = True
                    alell += 1
            else:
                individual = newPath + individual

        ##### se tem dois genes que não estão conectados                
        i = 0
        flag = False
        alell = 0
        while i < len(individual) - 1:
            if self.validateRoute(individual[i], individual[i + 1]) == False:
                possibilities = self.edgesV.get(individual[i])
                if len(possibilities) > 0:
                    chosen = random.choice(possibilities)
                    newPath = self.h_bfs(chosen, self.destino)
                    # newPath = self.h_astar(chosen,self.destino)
                    if newPath == "error":

                        while alell < i and flag == False:
                            newPath = self.h_bfs(individual[alell], individual[i + 1])
                            # newPath = self.h_astar(individual[alell],individual[i+1])
                            if newPath != "error":
                                individual = individual[:alell] + newPath + individual[i + 1:]
                                flag = True
                            alell += 1
                        if flag == False:
                            individual = self.h_bfs(self.inicio, self.destino)
                            # individual = self.h_astar(self.inicio,self.destino)
                    else:
                        individual = individual[:i + 1] + newPath
                else:
                    individual = self.h_bfs(self.inicio, self.destino)
                    # individual = self.h_astar(self.inicio,self.destino)

            i += 1

        ##### retirar genes repetidos
        repeated = self.setRepeated(individual)
        while len(repeated) > 0:
            new = []
            indices = [i for i, x in enumerate(individual) if x == repeated[0]]
            for j in range(len(individual)):
                if j >= indices[0] and j < indices[-1]:
                    pass
                else:
                    new.append(individual[j])
            individual = new
            repeated = self.setRepeated(individual)

        ##### se tem genes repetidos lado a lado
        n = 0
        while n < len(individual) - 1:
            if individual[n] == individual[n + 1]:
                individual.remove(individual[n])
            n += 1

        return individual

    def setRepeated(self, individual):
        repeated = []
        for i in range(0, len(individual)):
            if individual.count(str(individual[i])) > 1:
                repeated.append(str(individual[i]))
        return repeated

    def writeJson(self, content, file):
        with open(file + '.txt', 'w') as json_file:
            json.dump(content, json_file)

    def nextGeneration(self):

        before = copy.deepcopy(self.population)
        points = []
        generation = []

        # mutation
        amountIndividuals = 4
        typeMutation = 1
        selected = self.selectIndiv(amountIndividuals, before, self.fitness)
        for a in range(amountIndividuals):
            mutated = self.mutation(selected[a], typeMutation)
            generation.append(mutated)

        # crossover
        amountIndividuals = 2
        selected = self.selectIndiv(amountIndividuals, before, self.fitness)
        for a in range(0, amountIndividuals, 2):
            child1, child2 = self.crossover(selected[a], selected[a + 1])
            generation.append(child1)
            generation.append(child2)

        # best individual   
        bestIndiv = self.setBestIndividual(before)
        generation.append(self.getBestIndividual())
        errors = self.validatePop(generation)
        if len(errors) < 1:
            self.population = generation
        else:
            generation1 = []
            new = []
            for j in range(len(generation)):
                new = self.correct(generation[j])
                generation1.append(new)
                self.population = generation1

    def run(self):
        gen = 0
        self.setMatrix()
        self.setEdgesV1()
        self.setInitialPop()

        initial = self.population.copy()
        print("Population", self.population)
        while self.criterion != True:
            fitness = self.setFitnessPopulation(self.population)
            self.fitness = fitness
            self.nextGeneration()
            if gen == self.limit:
                self.criterion = True
            gen += 1
        print("initial pop", initial)
        print("Fitness last gen", self.fitness)
        print("The best route is:", self.getBestIndividual())
        print("The best fitness is:", self.bestFitness)
        return self.getBestIndividual()