from geny import population
import numpy as np
import copy
class GA(population):
    def __init__(self,*args,graph=None,canvas=None):
        super(GA,self).__init__(*args)
        self._graph = graph
        self._canvas = canvas
        self._currentPopulation_g = self._graph[0]
        self._currentPopulation_c=self._canvas[0]
        self._bestPopulation_c = self._canvas[1]
        self._bestPopulation_g = self._graph[1]

        self._BestFitness_c = self._canvas[3]
        self._BestFitness_g = self._graph[3]

        ##self._MeanFitness_c = self._canvas[4]
        #self._MeanFitness_g = self._graph[4]

        self.calcFitness()
        self.theBest=None
    def startGA(self,n_iterations = 100):

        print("Start GA")
        self.__fitnessScores = []
        self.__MeanfitnessScores = []
        self.__worstFitnessScores= []
        #fit = []
        for i in range(0,n_iterations):
            self.tournamentSelection()
            self.crossover()
            self.mutation()
            self.calcFitness()
            fit = []
            for y in self.pop:
                fit.append(y.fitness)
            self.__MeanfitnessScores.append(np.mean(fit))
            #print (self.__MeanfitnessScores)
            if len(self._graph)>0:
                self.graph(i)

    def graph(self,c=0):
        c+=1
       # copyPop = copy.deepcopy(self)
        self.sortByFitness()

        best = self.pop[0]
        worst = self.pop[-1]
        self.__fitnessScores.append(best.fitness)
        self.__worstFitnessScores.append(worst.fitness)

        if self.theBest == None:
            self.theBest = self.pop[0]
        try:
           if self.theBest.fitness < best.fitness:

               self.theBest = copy.deepcopy(self.pop[0])
               self._bestPopulation_g.clear()
               self._bestPopulation_g.plot([i.x for i in self.chromosome_list], [i.y for i in self.chromosome_list], 'ro')

               for i in self.chromosome_list:
                   self._bestPopulation_g.annotate(i.name, xy=(i.x, i.y), xytext=(i.x, i.y))
               self._bestPopulation_g.set_xlabel("X")
               self._bestPopulation_g.set_ylabel("Y")
               self._bestPopulation_g.grid(True, alpha=0.2, linewidth=1, pickradius=5)
               for i in range(0, len(self.theBest.route) - 1):
                   # print (best.route[i].x,best.route[i].y)

                   self._bestPopulation_g.plot([self.theBest.route[i].x, self.theBest.route[i + 1].x],
                                                  [self.theBest.route[i].y, self.theBest.route[i + 1].y],'g')
               self._bestPopulation_c.draw()
        except IndexError:
            self.theBest = best


        self._currentPopulation_g.set_title('Bierzaca populacja')

        self._currentPopulation_g.set_xlabel("X")
        self._currentPopulation_g.set_ylabel("Y")
        self._currentPopulation_g.clear()
        self._currentPopulation_g.grid(True,alpha=0.2,linewidth=1, pickradius=5)

        #self._BestFitness_g.clear()
        self._BestFitness_g.set_title('Bierzaca populacja')
        self._BestFitness_g.set_xlabel("Epoch")
        self._BestFitness_g.set_ylabel("Fitness")

        self._BestFitness_g.grid(True,alpha=0.2,linewidth=1, pickradius=5)
        #for c,i in list(enumerate(self.__fitnessScores)):
        #    self._BestFitness_g.plot(c,i,'ro')
        #for c,i in list(enumerate(self.__MeanfitnessScores)):
        #    self._BestFitness_g.plot(c, i, 'go')
        #for c,i in list(enumerate(self.__worstFitnessScores)):
        #    self._BestFitness_g.plot(c, i, 'bo')
        #    self._BestFitness_g.plot(c,len(self.pop),'y')
        #self._BestFitness_c.draw()
        self._BestFitness_g.plot(c, self.__fitnessScores[-1], 'ro')
        self._BestFitness_g.plot(c, self.__MeanfitnessScores[-1], 'bo')
        self._BestFitness_g.plot(c, self.__worstFitnessScores[-1], 'yo')
        #print(len(self.pop))
        #self._BestFitness_g.plot(c, len(self.pop), 'g-')
        self._BestFitness_c.draw()

        _x = [i.x for i in self.chromosome_list]
        _y = [i.y for i in self.chromosome_list]
        self._currentPopulation_g.plot(_x,_y, 'ro')
        for i in self.chromosome_list:
            self._currentPopulation_g.annotate(i.name, xy=(i.x, i.y), xytext = (i.x, i.y))
        for i in range(0,len(best.route)-1):
            self._currentPopulation_g.plot([best.route[i].x, best.route[i+1].x], [best.route[i].y, best.route[i+1].y],'g')
            self._currentPopulation_g.plot([worst.route[i].x, worst.route[i + 1].x], [worst.route[i].y, worst.route[i + 1].y], 'r')
        self._currentPopulation_c.draw()