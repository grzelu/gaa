from geny import population
import numpy as np
import copy



class GA(population):
    def __init__(self,*args,
                 graph=None,canvas=None,
                 windows=None,
                 test="TEST",
                 tournament_select=5,
                 tournament_size=3,
                 randomPopulation,
                 elitism=0,
                 selectOption="Tournament Selection",
                 mutationOptions = "shuffle",startCounter=0,crossoverOptions = "Random Points"):
        super(GA,self).__init__(*args,randomPopulation,test)
        self.startCounter = startCounter
        self.tournament_size = tournament_size
        self.tournament_select = tournament_select
        self.selectOption = selectOption
        self._graph = graph
        self._canvas = canvas
        self.elitism = elitism
        self._crossoverOption = crossoverOptions
        self.mutationOptions = mutationOptions
        print(self._crossoverOption)
        self._currentPopulation_g = self._graph[0]
        self._currentPopulation_c=self._canvas[0]
        self._bestPopulation_c = self._canvas[1]
        self._bestPopulation_g = self._graph[1]

        self._BestFitness_c = self._canvas[2]
        self._BestFitness_g = self._graph[2]
        self.populationwindow = windows[0]
        self.fistpopulationwindow = windows[1]
        #print (self.populationwindow)
        ##self._MeanFitness_c = self._canvas[4]
        #self._MeanFitness_g = self._graph[4]

        self.calcFitness()
        self.theBest=None

    def makePopulationLabelText(self,firstgeneration=False):
        text=""


        for i in self.pop:
            text = text + str(i) + "\n"
        if firstgeneration == False:
            self.populationwindow.config(text=text)
        elif firstgeneration==True:
            self.fistpopulationwindow.config(text=text)
    def crossover(self):
        if self._crossoverOption == "Random Points":
            self.crossover_RandomPoints()
        elif self._crossoverOption == "One Point of Crossing":
            self.crossover_pointOfCross()
        elif self._crossoverOption == "Two Point of Crossing":
            self.crossover_twoPointsofCrossing()

    def selection(self):
        if self.selectOption== "Tournament Selection":
            self.tournamentSelection(tournamentsize=self.tournament_size, numberToSelect=self.tournament_select,
                                  choosen=[])
        elif self.selectOption == "Random":
            self.randomSelect(numberToSelect = self.tournament_select)
        elif self.selectOption == "Best":
            self.selection_BestHalf(numberToSelect=self.tournament_select)

    def startGA(self,n_iterations = 100):
        self.makePopulationLabelText(firstgeneration=True)
        self.__fitnessScores = []
        self.__MeanfitnessScores = []
        self.__worstFitnessScores= []
        for i in range(0,n_iterations):
            self.makePopulationLabelText()
            self.selection()
            #self.removeDuplicates()
            self.crossover()
            #self.removeDuplicates()
            self.mutation(self.mutationOptions)
            self.calcFitness()
            self.makePopulationLabelText()
            self.sortByFitness()

            fit = []
            if self.elitism == 1:
                self.sortByFitness()
                if self.theBest == None:
                    self.theBest = self.pop[0]
                else:
                    self.pop.append(self.theBest)
            for y in self.pop:
                #print(y)
                fit.append(round(y.fitness,3))
            self.__MeanfitnessScores.append(np.mean(fit))
            if len(self._graph)>0:
                self.graph(i)



    def drawBest(self,epoch):
        self._bestPopulation_g.clear()
        self._bestPopulation_g.set_title('Best solution so far')

        self._bestPopulation_g.plot([i.x for i in self.chromosome_list], [i.y for i in self.chromosome_list], 'ro')

        best = self.pop[0]
        worst = self.pop[-1]
        for i in self.chromosome_list:
            self._bestPopulation_g.annotate(i.name, xy=(i.x, i.y), xytext=(i.x, i.y))
        self._bestPopulation_g.set_xlabel("X Epoch:{} {}".format(epoch,self.theBest))
        self._bestPopulation_g.set_ylabel("Y")
        self._bestPopulation_g.grid(True, alpha=0.2, linewidth=1, pickradius=5)
        for i in range(0, len(self.theBest.route) - 1):
            #print(best.route[i].x, best.route[i].y)
            self._bestPopulation_g.legend(['City','Best route'])
            self._bestPopulation_g.plot([self.theBest.route[i].x, self.theBest.route[i + 1].x],
                                        [self.theBest.route[i].y, self.theBest.route[i + 1].y], 'g')
        self._bestPopulation_c.draw()

    def graph(self,c=0):
        c+=1
        self.sortByFitness()

        best = self.pop[0]
        worst = self.pop[-1]

        if self.theBest == None:
            self.theBest = self.pop[0]
            self.drawBest(c)
        try:
           if self.theBest.fitness > best.fitness:

               self.theBest = copy.deepcopy(self.pop[0])
               self.drawBest(c)
        except IndexError:
            self.theBest = best

        self.__fitnessScores.append(best.fitness)
        self.__worstFitnessScores.append(worst.fitness)
        self._currentPopulation_g.clear()
        self._currentPopulation_g.set_title('Current population BEST(g)/WORST(r)')
        self._currentPopulation_g.set_ylabel("Y")
        self._currentPopulation_g.set_xlabel("X")
        self._currentPopulation_g.grid(True,alpha=0.2,linewidth=1, pickradius=5)


        self._BestFitness_g.set_title('Fitness')
        self._BestFitness_g.set_xlabel("Epoch")
        self._BestFitness_g.set_ylabel("Fitness")
        self._BestFitness_g.grid(True,alpha=0.2,linewidth=1, pickradius=5)
        self._BestFitness_g.plot(c, self.__fitnessScores[-1], 'ro')
        self._BestFitness_g.plot(c, self.__MeanfitnessScores[-1], 'bo')
        self._BestFitness_g.legend(['Best score', 'Mean score'])
        self._BestFitness_c.draw()

        _x = [i.x for i in self.chromosome_list]
        _y = [i.y for i in self.chromosome_list]
        self._currentPopulation_g.plot(_x,_y, 'ro')
        for i in self.chromosome_list:
            self._currentPopulation_g.annotate(i.name, xy=(i.x, i.y), xytext = (i.x, i.y))
        for i in range(0,len(best.route)-1):
            self._currentPopulation_g.plot([best.route[i].x, best.route[i+1].x], [best.route[i].y, best.route[i+1].y],'g')
            self._currentPopulation_g.plot([worst.route[i].x, worst.route[i + 1].x], [worst.route[i].y, worst.route[i + 1].y], 'r')
            self._currentPopulation_g.legend(['City', 'Best route', 'Worst route'])
        self._currentPopulation_c.draw()


