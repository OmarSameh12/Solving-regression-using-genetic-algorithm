import random

from Chromosome import Chromosome


class GA:
    def __init__(self, psize):
        self.psize = psize
        self.pop = []
        self.parents = []
        self.children = []
        self.x_array = []
        self.y_array = []
        self.pc = 0.8
        self.pm = 0.01
        self.k = 2
        self.lowBound = -10
        self.uppBound = 10
        self. offspring = []
        self.selectedParentsIndex=[]
    def initialize_population(self, num_of_coff, psize):
        print("The Initialized Population")
        for i in range(psize):
            # numOfItems is the coefficients
            ch = Chromosome(num_of_coff)
            ch.initialize()
            self.pop.append(ch)

    def calcFitness(self, numdatapts, xarray, yarray):
        print("\nThe Calculated fitness of the population\n")
        for x in range(len(self.pop)):
            self.pop[x].calcFitnessVal(numdatapts, xarray, yarray)
            self.pop[x].printChData()

    def selection(self):
        #To empty the parents list for new iteration
        self.parents.clear()
        kparents=[]
        self.selectedParentsIndex.clear()
        # Select no. of parents by tournament selection
        half_the_pop=int(self.psize/2)
        for j in range(half_the_pop):
            kparents.clear()
            for i in range(self.k):
                choice = random.randint(0, self.psize - 1)
                #variable choice in chromosome is to know the index of chromosome in population so it can be removed in the replacment step
                self.pop[choice].index=choice
                kparents.append(self.pop[choice])
            kparents.sort(key=lambda kparents: kparents.fitnessvalue)
            self.selectedParentsIndex.append(kparents[-1].index)
            self.parents.append(kparents[-1])

        print("\nThe Selected Parents\n")
        for x in range(len(self.parents)):
            self.parents[x].printChData()

    def crossover(self, numdatapts, xarray, yarray):
        self.offspring.clear()
        # ***Start the Crossover*** #
        self.parents.sort(key=lambda kparents: kparents.fitnessvalue)
        for i in range(0, int(len(self.parents)/2 ), 1):
            p1 = self.parents[i]
            j=i+1
            p2 = self.parents[j]
            xc = (random.randint(1, 10) / 10)
            if xc < self.pc:
                x = []
                y = []
                point1 = random.randint(1, len(self.pop[0].genes) - 1)
                point2 = random.randint(1, len(self.pop[0].genes) - 1)
                if point1 > point2:
                    temp = point1
                    point1 = point2
                    point2 = temp
                for j in range(len(self.pop[0].genes)):
                    if j < point1 or j >= point2:
                        x.append(p1.genes[j])
                        y.append(p2.genes[j])
                    else:
                        x.append(p2.genes[j])
                        y.append(p1.genes[j])
                self.offspring.append(Chromosome(len(self.pop[0].genes)))
                self.offspring[-1].setGenes(x)
                self.offspring[-1].calcFitnessVal(numdatapts, xarray, yarray)
                self.offspring.append(Chromosome(len(self.pop[0].genes)))
                self.offspring[-1].setGenes(y)
                self.offspring[-1].calcFitnessVal(numdatapts, xarray, yarray)

            else:
                self.offspring.append(p1)
                self.offspring.append(p2)
        print("\nOffsprings are\n")
        print("Size of them is ", len(self.offspring))
        for i in range(len(self.offspring)):
            print(self.offspring[i].printChData())



    def mutation(self, no_generation, current_generation):
        print("\nOffsprings after Mutation")
        for i in range(len(self.offspring)):
            for j in range(len(self.pop[0].genes)):
                if random.random() <= self.pm:
                    delta_low = self.offspring[i].genes[j] - self.lowBound
                    delta_upp = self.uppBound - self.offspring[i].genes[j]

                    if random.random() <= 0.5:
                        Y = delta_low
                    else:
                        Y = delta_upp
                    r = random.random()
                    t = current_generation
                    T = no_generation
                    b = random.uniform(0.5, 5)
                    delta_change = Y * (1 - r ** (1 - t / T) ** b)

                    if Y == delta_low:
                        self.offspring[i].genes[j] = self.offspring[i].genes[j] - delta_change
                    else:
                        self.offspring[i].genes[j] = delta_change + self.offspring[i].genes[j]
        print(len(self.offspring))
        for i in range(len(self.offspring)):
            print(self.offspring[i].printChData())

    def elitist_Replacment(self):
        #removing the repeated selected parents index
        self.selectedParentsIndex = list(dict.fromkeys(self.selectedParentsIndex))
        #n is the number of best individuals selected from parents and removed from population
        n=2
        #The number of unique parents selected from population
        nselectedpar=len(self.selectedParentsIndex)
        best_n_parents=[]
        # Select the best n parents from the parent array
        self.parents.sort(key=lambda parents: parents.fitnessvalue)
        #loop is to get the best n individuals from sorted parents array (from end of array)j equation is to map iterations into - value to get values from end of array
        for i in range(n):
            j=i*-1
            j-=1
            best_n_parents.append(self.parents[j])
        #Removing previously selected parents using selectedparentsindex filled in the selection step
        self.selectedParentsIndex.sort(reverse=True)
        for q in range(nselectedpar):
            self.pop.pop(self.selectedParentsIndex[q])

        # Adding offspring to pop
        self.pop+=self.offspring
        # Delete the worst n and append the best n
        self.pop.sort(key=lambda pop: pop.fitnessvalue)
        diff=len(self.pop)-self.psize
        for k in range(diff+n):
            self.pop.pop(0)
        self.pop+=best_n_parents

        print("Size of population after all changes is ",len(self.pop))
    def printPopulation(self):
        print("The population after removing worst n individuals and adding best n parents \n")
        for i in range(len(self.pop)):
            self.pop[i].printChData()
        return

    def findBestSol(self):
        self.pop.sort(key=lambda kparents: kparents.fitnessvalue)
        print("\nBest solution is with paramenters : ")
        self.pop[-1].printChData()

    def findBest(self):
        self.pop.sort(key=lambda kparents: kparents.fitnessvalue)
        return self.pop[-1].bestsol()

    def run(self, nOfGenerations, degree, numdatapts, xarray, yarray):
        numOfIteration = (int)(self.psize / 2)
        for current_generation in range(nOfGenerations):
            print("Iteration num ", current_generation + 1)

            if current_generation == 0:
                self.initialize_population(degree+1 , self.psize)
            for j in range(numOfIteration):
                self.calcFitness(numdatapts, xarray, yarray)
                self.selection()
                self.crossover(numdatapts, xarray, yarray)
                self.mutation(nOfGenerations, current_generation)
                self.elitist_Replacment()
                self.printPopulation()
        self.findBestSol()


