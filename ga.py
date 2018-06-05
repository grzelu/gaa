from geny import population

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

        self.calcFitness()
        self.theBest=None
    def startGA(self,n_iterations = 100):

        print("Start GA")
        self.__fitnessScores = []
        for i in range(0,n_iterations):
            self.tournamentSelection()
            self.crossover()
            self.mutation()
            self.calcFitness()
            if len(self._graph)>0:
                self.graph()

    def graph(self):

       # copyPop = copy.deepcopy(self)
        self.sortByFitness()

        best = self.pop[0]
        self.__fitnessScores.append(best.fitness)

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
                                                  [self.theBest.route[i].y, self.theBest.route[i + 1].y])
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
        for c,i in list(enumerate(self.__fitnessScores)):
            self._BestFitness_g.plot(c,i,'ro')
        self._BestFitness_c.draw()


        _x = [i.x for i in self.chromosome_list]
        _y = [i.y for i in self.chromosome_list]
        self._currentPopulation_g.plot(_x,_y, 'ro')
        for i in self.chromosome_list:
            self._currentPopulation_g.annotate(i.name, xy=(i.x, i.y), xytext = (i.x, i.y))
        for i in range(0,len(best.route)-1):
            self._currentPopulation_g.plot([best.route[i].x, best.route[i+1].x], [best.route[i].y, best.route[i+1].y])
        self._currentPopulation_c.draw()