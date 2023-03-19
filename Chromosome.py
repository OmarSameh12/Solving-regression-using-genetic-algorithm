import random


class Chromosome:
    def __init__(self, degree):
        self.degree = degree
        self.genes = []
        self.fitnessvalue=0
        self.expectedy = 0
        self.index=-1
        self.mse=-1


    def initialize(self):
        for i in range(self.degree):
            p = (random.uniform(-10, 10))
            self.genes.append(p)

        print(self.genes)

    def calcFitnessVal(self,numdatapts,xarray, yarray):
        error = 0

        for i in range(numdatapts):

            for j in range(self.degree):
                self.expectedy += (self.genes[j] * (xarray[i] ** j))
            error += ((self.expectedy - yarray[i]) ** 2)

        self.mse= error / numdatapts
        self.fitnessvalue = 1 / self.mse

    def setGenes(self, genes):
        self.genes = genes

    def printChData(self):
        print(self.genes)
        print('The mean square error value is = ',self.mse)
        return " "

    def bestsol(self):
        return self.genes,  'The Mean square error value is = ', self.mse
