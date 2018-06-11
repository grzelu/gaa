import numpy as np
import random
import copy
data_path = "DANE.txt"
data_matrix = np.loadtxt(data_path,skiprows=25)
flow_matrix = data_matrix
data_file = open(data_path,'r')
city_list = []
flow_list = []
flow=False
counter = 0

while True:

    line = data_file.readline().strip('\r\n')
    #print(line)
    if line=='---':
        data_file.close()
        break
    temp = line.split(' ')
    city_list.append({'idx':counter, 'name':temp[0],'x':temp[1],'y':temp[2]})
    counter += 1

class city():
    def __str__(self):
        return "%s idx:%s" % (self.name, self.idx)
    def __repr__(self):
        return "%s idx:%s" % (self.name, self.idx)
    def __init__(self, data, flow_matrix):
        self.name = data['name']
        self.x = int(data['x'])
        self.y = int(data['y'])
        self.idx = data['idx']
        self.flow_matrix = flow_matrix
    def distanceTo(self,city):
        return np.sqrt(abs((city.x-self.x))^2+abs((city.y-self.y))^2)

    def speedLimitTo(self,city):
        return self.flow_matrix[self.idx][city.idx]

class route:
    _counter = 1
    def __init__(self, routeSize,chromosome_list,randomPop, counter):
        self.route = [chromosome_list[0]]
        self.route.extend(random.sample(chromosome_list[1:-1], routeSize - 2))
        self.route.extend(chromosome_list[-1:])
        self.fitness = 0
        self.n_fitness = 0

    def calcFitness(self):
        self.fitness=0;
        dist=0
        totaltime=0
        vmaxall=0
        for i in range(0,len(self.route)-1):
            dst = self.route[i].distanceTo(self.route[i+1])*1
            vmax = self.route[i].speedLimitTo(self.route[i+1])
            dist=dist+dst
            vmaxall=vmaxall+vmax
            time = dst/vmax
            totaltime = totaltime + time

            self.fitness+=time

        self.fitness = self.fitness*100


    def __str__(self):
        string = "F:{} ".format(round(self.fitness),2)
        for i in self.route:

            string = string + "[{}] ".format(i.idx)
        return string

    def __repr__(self):
        return self.__str__()
chromosome_list = [city(i, flow_matrix) for i in city_list]

class population(list):
    def __init__(self,chromosome_list, populationSize, route_size,crossover_probability, mutation_probability,randomPopulation = False,test="TEST"):
        self.route_size=route_size
        self.counter=0
        self.populationSize = populationSize
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.chromosome_list = chromosome_list
        self.pop=[]
        [self.pop.append(route(route_size, chromosome_list,randomPopulation,counter=self.counter)) for i in range(0, populationSize)]

        self.selected=[]
    def calcFitness(self):
        [i.calcFitness() for i in self.pop]
    def removeDuplicates(self):
        lenpop = len(self.pop)
        x = self.pop
        xx = set(self.pop)
        lenset = len(xx)
        npop = []
        for i in xx:
            npop.append(i)
        self.pop= npop
    def normalizeFitness(self):
        allFitness = 0
        n_fit = 0
        for i in self.pop:
            allFitness += i.fitness

        for i in self.pop:
            i.n_fitness = i.fitness / allFitness
        self.meanFitness = allFitness/len(self.pop)
    def sortByFitness(self):
        self.pop.sort(key=lambda x: x.fitness, reverse=False)
    def mutation(self,mutationOptions):

        mutate = []
        mutation_method = mutationOptions
        #print (mutation_method)
        for i in self.pop:
            rand = random.uniform(0,1)
            if rand < self.mutation_probability:
              #  print("MUTATION")
                #print (rand)
                method = random.choice(mutation_method)

                mutate.append({"route":i, "method":method})
                #print(len(mutate))
        for i in mutate:
            #print(mutationOptions)
            if i['method'] == 'swapPosition':
                print("SWAP POSITION")
                toSwap = random.sample(range(1,len(i['route'].route)-1),2)
                _cpy = copy.deepcopy(i['route'])
                i['route'].route[toSwap[0]] = _cpy.route[toSwap[1]]
                i['route'].route[toSwap[1]] = _cpy.route[toSwap[0]]
                i['route'].calcFitness()
            elif i['method'] == 'changeOne':
                print("CHANGE ONE")
                toChange = random.randint(1,len(i['route'].route)-1)
               # print (toChange)
                #print(len(i['route'].route))
                __ch_list = copy.deepcopy(self.chromosome_list)
                ch_list = __ch_list[1:-1]
                random.shuffle(ch_list)
                #print(ch_list)
                for chr in ch_list:
                    isValid = True
                    #print(list(range(1, len(i['route'].route) - 1)))
                    for y in range(1,len(i['route'].route)-1):
                        if chr.idx==i['route'].route[y].idx:
                            isValid= False
                    if isValid == True:
                        if int(chr.idx) == 23:
                            continue
                        if int(i['route'].route[toChange].idx) == 23:
                            continue
                        #print (chr,i['route'].route[toChange])
                        i['route'].route[toChange] = chr
                        i['route'].calcFitness()
                        break
            elif i['method'] == 'changeMore':
                print("CHANGE MORE")
                rang = range(1,len(i['route'].route)-1)
                count = random.randint(1,len(i['route'].route)-2)
                _toChange = random.sample(rang,count)
               # print (toChange)
                #print(len(i['route'].route))
                __ch_list = copy.deepcopy(self.chromosome_list)
                ch_list = __ch_list[1:-1]
                random.shuffle(ch_list)
                #print(ch_list)
               # print("BEFORE",i['route'])
                for toChange in _toChange:
                    for chr in ch_list:
                        isValid = True
                        #print(list(range(1, len(i['route'].route) - 1)))
                        for y in range(1,len(i['route'].route)-1):
                            if chr.idx==i['route'].route[y].idx:
                                isValid= False
                        if isValid == True:
                            if int(chr.idx) == 23:
                                continue
                            if int(i['route'].route[toChange].idx) == 23:
                                continue
                            #print (chr,i['route'].route[toChange])
                            i['route'].route[toChange] = chr
                            i['route'].calcFitness()
                            break
                #print("AFTER", i['route'])
            elif i['method'] == 'shuffle':
                print("SHUFLE")
                chr = copy.deepcopy(i['route'])
                chrroute = chr.route[1:-1]
                random.shuffle(chrroute)
                _tab = list(range(1,len(i['route'].route)-1))
                _2tab = list(range(1,len(i['route'].route)-1))
                random.shuffle(_2tab)
                for c in _tab:
                    i['route'].route[c] = chrroute[c - 1]
                i['route'].calcFitness()

    def selection_BestHalf(self,numberToSelect=50):
        self.choosen=[]
        self.sortByFitness()
        popsize = len(self.pop)
        for i in range(0,numberToSelect):
            self.choosen.append(self.pop.pop(i))

    def randomSelect(self,numberToSelect=50):
        self.choosen=[]
        x = self.pop
        random.shuffle(x)
        for i in range(0,numberToSelect):
            self.choosen.append(self.pop.pop())


    def trnSelect(self,tournamentMembers):
        best = None
        rest = []
        for i in tournamentMembers:
            if best == None:
                best = i
            if i.fitness < best.fitness:
                best = i
            else:
                rest.append(i)
        return best,rest



    def tournamentSelection(self,tournamentsize=5, numberToSelect=50,choosen=[]):
        tournamentMembers = []
        if numberToSelect == 0:
           # print(len(self.pop), len(choosen))
            self.choosen = choosen
            self.pop = self.pop + self.choosen
            return self.choosen
        for i in range(0,tournamentsize):
            member = self.pop[random.randint(0,len(self.pop)-1)]
            tournamentMembers.append(member)

        best,rest = self.trnSelect(tournamentMembers)

        self.pop.remove(best)

        if best in self.pop:
            return
            self.tournamentSelection(tournamentsize=tournamentsize, numberToSelect=numberToSelect, choosen=choosen)
        choosen.append(best)
        self.tournamentSelection(tournamentsize = tournamentsize, numberToSelect = numberToSelect-1, choosen = choosen)


    def crossover_RandomPoints(self):
        if self.crossover_probability == 0:
            self.choosen=[]
            return
        new_population=[]
        for i in self.choosen:
            x=random.uniform(0,1)
            if float(self.crossover_probability) < x:
                new_population.append(self.choosen.pop())
        counter=0
        while len(self.choosen)>2:
            try:
                ch1 = copy.deepcopy(self.choosen[counter])
                ch2 = copy.deepcopy(self.choosen[counter+1])
            except IndexError:
                if ch1:
                    break
                else:
                    break
            counter+=2

            crossPoints = random.sample(range(1, self.route_size - 1), random.randint(0, self.route_size - 2))
            for i in crossPoints:
                status=1
                for y in ch1.route:
                    if y.idx == ch2.route[i].idx:
                        status=0
                if status == 1:
                    ch1.route[i] = ch2.route[i]
            ch1.calcFitness()

            new_population.append(ch1)
        self.pop.extend(new_population)
        self.pop.extend(self.choosen)
        self.sortByFitness()
        self.removeDuplicates()
        self.pop = self.pop[:self.populationSize]

    def crossover_twoPointsofCrossing(self):
        if self.crossover_probability == 0:
            self.choosen=[]
            return
        new_population=[]
        for i in self.choosen:
            x=random.uniform(0,1)
            if float(self.crossover_probability) < x:
                new_population.append(self.choosen.pop())
        counter=0
        while len(self.choosen)>2:
            try:
                ch1 = copy.deepcopy(self.choosen[counter])
                ch2 = copy.deepcopy(self.choosen[counter+1])
            except IndexError:
                if ch1:
                    break
                else:
                    break
            counter+=2
            left = random.randint(1,self.route_size-2)
            right = random.randint(left,self.route_size-1)

            crossPoints = list(range(left,right))
            for i in crossPoints:
                status=1
                for y in ch1.route:
                    if y.idx == ch2.route[i].idx:
                        status=0
                if status == 1:
                    ch1.route[i] = ch2.route[i]
            ch1.calcFitness()

            new_population.append(ch1)
        self.pop.extend(new_population)
        self.pop.extend(self.choosen)
        self.sortByFitness()
        #self.removeDuplicates()
        self.pop = self.pop[:self.populationSize]

    def crossover_pointOfCross(self):
        if self.crossover_probability == 0:
            self.choosen=[]
            return
        new_population=[]
        for i in self.choosen:
            x=random.uniform(0,1)
            if float(self.crossover_probability) < x:
                new_population.append(self.choosen.pop())
        counter=0
        while len(self.choosen)>2:
            try:
                ch1 = copy.deepcopy(self.choosen[counter])
                ch2 = copy.deepcopy(self.choosen[counter+1])
            except IndexError:
                if ch1:
                    break
                else:
                    break
            counter+=2

            crossPoints = range(1,random.randint(1,self.route_size-1))
            for i in crossPoints:
                status=1
                for y in ch1.route:
                    if y.idx == ch2.route[i].idx:
                        status=0
                if status == 1:
                    ch1.route[i] = ch2.route[i]
            ch1.calcFitness()

            new_population.append(ch1)
        self.pop.extend(new_population)
        self.pop.extend(self.choosen)
        self.sortByFitness()
        self.removeDuplicates()
        self.pop = self.pop[:self.populationSize]


