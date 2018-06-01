from geny import population


class GA(population):
    def __init__(self,*args,graph=None,canvas=None):
        print ("DDDDDD")
        super(GA,self).__init__(*args)
        self._graph=graph
        self.canvas=canvas
        self.calcFitness()

    def startGA(self,n_iterations = 100):
        print(self.pop)
        print("Start GA")
        for i in range(0,n_iterations):
            self.tournamentSelection()
            self.crossover()
            self.mutation()
            self.calcFitness()
            if self._graph:
                self.graph()
            #print (self.pop)
    def graph(self):

       # copyPop = copy.deepcopy(self)
        self.sortByFitness()
        best = self.pop[0]

        self._graph.set_title('Bierzaca populacja')

        self._graph.set_xlabel("X")
        self._graph.set_ylabel("Y")
        self._graph.clear()
        self._graph.grid(True,alpha=0.2,linewidth=1, pickradius=5)
        print (best)
        _x = [i.x for i in self.chromosome_list]
        _y = [i.y for i in self.chromosome_list]
        self._graph.plot(_x,_y, 'ro')
        for i in self.chromosome_list:
            self._graph.annotate(i.name, xy=(i.x, i.y), xytext = (i.x, i.y))
        for i in range(0,len(best.route)-1):
            #print (best.route[i].x,best.route[i].y)

            self._graph.plot([best.route[i].x, best.route[i+1].x], [best.route[i].y, best.route[i+1].y])
            self.canvas.draw()