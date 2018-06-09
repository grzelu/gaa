import numpy as np
import random
import copy
data_path = "DANE.txt"
data_matrix = np.loadtxt(data_path,skiprows=25)
flow_matrix = data_matrix
#print (flow_matrix)

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

    #city_list.append(.append(counter))
    city_list.append({'idx':counter, 'name':temp[0],'x':temp[1],'y':temp[2]})
    counter += 1

class city():
    def __str__(self):
        #return "%s idx:%s x:%s y:%s" % (self.name,self.idx,self.x,self.y)
        return "%s idx:%s x:%s y:%s" % (self.name, self.idx, self.x, self.y)
    def __repr__(self):
        return "%s idx:%s x:%s y:%s" % (self.name, self.idx, self.x, self.y)
    def __init__(self, data, flow_matrix):
        self.name = data['name']
        self.x = int(data['x'])
        self.y = int(data['y'])
        self.idx = data['idx']
        self.flow_matrix = flow_matrix
    def distanceTo(self,city):
        return round(np.sqrt(abs((city.x-self.x))^2+abs((city.y-self.y))^2))*10

    def speedLimitTo(self,city):
        return self.flow_matrix[self.idx][city.idx]

class route:
    _counter = 1
    def __init__(self, routeSize,chromosome_list,randomPop, counter):
        self.route = [chromosome_list[0]]
        #print('RITUAEDASDAS',randomPop)
        if randomPop == 1:
            if route._counter==0 or route._counter==routeSize:
                route._counter=1
            #x = copy.deepcopy(chromosome_list)

            self.route.extend(random.sample(chromosome_list[1:-1], routeSize-2))
            #self.route.extend(chromosome_list[-1:])
        else:
            for i in range(0,routeSize-2):
                self.route.append(chromosome_list[route._counter])
                route._counter =route._counter+1
                if route._counter == len(chromosome_list):
                    route._counter=1
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
            vmax = self.route[i].speedLimitTo(self.route[i+1])*3
            dist=dist+dst
            vmaxall=vmaxall+vmax
            time = dst/vmax
            totaltime = totaltime + time
            #print ("Time: {} = Dist: {} / Speed: {}".format(time,dst,vmax))
            self.fitness+=time
        #print (dist,'/' ,totaltime,"=",dist/totaltime,self.fitness)
        self.fitness = self.fitness*(dist/totaltime)


    def __str__(self):
        string = "F:{} ".format(round(self.fitness))
        for i in self.route:
            #string = string + "[{}]{} ".format(i.idx,i.name)
            string = string + "[{}] ".format(i.idx)
        return string

    def __repr__(self):
        return self.__str__()
chromosome_list = [city(i, flow_matrix) for i in city_list]

class population(list):
    def __init__(self,chromosome_list, populationSize, route_size,crossover_probability, mutation_probability,randomPopulation = False,test="TEST"):
       # print("GENERATE RANDOM",randomPopulation,test)
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
       # print("CALCULATE FITNESS")
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
        print ("REMOVED {} duplacates".format(lenpop-lenset))
    def normalizeFitness(self):
        allFitness = 0
        n_fit = 0
        for i in self.pop:
            allFitness += i.fitness

        for i in self.pop:
            i.n_fitness = i.fitness / allFitness
        self.meanFitness = allFitness/self.populationSize
    def sortByFitness(self):
        self.pop.sort(key=lambda x: x.fitness, reverse=False)
    def mutation(self):

        mutate = []
        mutation_method = ['shuffle']
       # mutation_method = ['swapPosition', 'changeOne','shuffle']
        #mutation_method = ['swapPosition','changeOne','changeMore']
        #mutation_method = ['changeMore']
        for i in self.pop:
            rand = random.uniform(0,1)
            if rand < self.mutation_probability:
              #  print("MUTATION")
                method = random.choice(mutation_method)
               # print ('mutuje',i,self.mutation_probability, method, rand)
                mutate.append({"route":i, "method":method})
        for i in mutate:
            if i['method'] == 'swapPosition':
                toSwap = random.sample(range(1,len(i['route'].route)-1),2)
              #  print (toSwap)
                _cpy = copy.deepcopy(i['route'])
                #print (i['route'].route)
                i['route'].route[toSwap[0]] = _cpy.route[toSwap[1]]
                i['route'].route[toSwap[1]] = _cpy.route[toSwap[0]]
                #print(i['route'].route)
            elif i['method'] == 'changeOne':
                toChange = random.randint(1,len(i['route'].route)-1)
                __ch_list = copy.deepcopy(self.chromosome_list)
                ch_list = __ch_list[1:-1]
                random.shuffle(ch_list)
               # print (i['route'].route)
                for chr in ch_list:
                    isValid = True
                    for y in range(1,len(i['route'].route)-2):
                    #for city in chr[1:-1]
                        if city==i['route'].route[y]:
                            isValid= False
                    if isValid == True:
                        i['route'].route[toChange] = chr
                        break

            elif i['method'] == 'shuffle':
              #  print ("przed sszufle",i['route'].route)
                chr = copy.deepcopy(i['route'])
                chrroute = chr.route[1:-1]
                random.shuffle(chrroute)
                _tab = list(range(1,len(i['route'].route)-1))
                _2tab = list(range(1,len(i['route'].route)-1))
               # print(_2tab)
                random.shuffle(_2tab)
              #  print(_2tab)
                for c in _tab:
                    i['route'].route[c] = chrroute[c - 1]
                   # print(i['route'].route[c],chr.route[_tab[y]],"xd")


               # print ("poddd szufle",i['route'].route)
                #valuesToChange = random.sample(range(1,len(i['route'].route) - 1),amountToChange)
                #print (valuesToChange)


    def selection_BestHalf(self):
        self.sortByFitness()
        popsize = len(self.pop)
        halfpop= int(popsize/2)
        self.choosen = self.pop[:halfpop]
        self.notChoosen = self.pop[halfpop:]
        #for i in self.choosen:
        #    print ('chosen',i.fitness)
        #for i in self.notChoosen:
        #    print ('notchosen',i.fitness)

    def tournamentSelection(self):
        #print ("Tournament selection")
        #temp  = copy.deepcopy(self.pop)
        self.notChoosen=[]
        random.shuffle(temp)
        self.choosen = []
        final = []
        while len(self.pop)>1:
            ch1 = self.pop.pop()
            ch2 = self.pop.pop()
            #print (ch1.fitness,"VS", ch2.fitness)
            if ch1.fitness < ch2.fitness:
                #print ('win',ch1.fitness)
                self.choosen.append(ch1)
                self.notChoosen.append(ch2)
            else:
                #print('win', ch2.fitness)
                self.choosen.append(ch2)
                self.notChoosen.append(ch1)
        #while len(choosen)>1:
        #    ch1 = choosen.pop()
        #    ch2 = choosen.pop()
        #    if ch1.fitness < ch2.fitness:
        #        final.append(ch1)
        #    else:
        #        final.append(ch2)
       # print (final,len(self.notChoosen))
        self.notChoosen.sort(key=lambda x: x.fitness, reverse=False)
        #for i in self.notChoosen:
           # print (i.fitness)

        return self.choosen

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
        #print ("BEST",best)
        return best,rest



    def tournamentSelection2(self,tournamentsize=3, numberToSelect=5,choosen=[]):
        x= self.pop
        tournamentMembers = []
        if numberToSelect == 0:
            print ("WYCHODZE")
            self.choosen = choosen
            self.pop = self.pop + self.choosen
            print (self.choosen)
            #self.notChoosen = list(set(self.pop)^set(self.choosen))
            self.notChoosen = self.pop

            print(len(self.pop),len(self.choosen),len(self.notChoosen))
            return self.choosen
        for i in range(0,tournamentsize):
            member = self.pop[random.randint(0,len(self.pop)-1)]
            tournamentMembers.append(member)
        #print (tournamentMembers)
        best,rest = self.trnSelect(tournamentMembers)
        #print ("Before",len(self.pop))
        self.pop.remove(best)
        #print("After", len(self.pop))
        #for _rest in rest:
        #    if _rest not in self.pop:
        #        self.pop.append(_rest)
        #    else:
        #        print ("REST JZU JEST")
        if best in self.pop:
            print ("TO JUZ JEST!!!")
            return
            self.tournamentSelection2(tournamentsize=tournamentsize, numberToSelect=numberToSelect, choosen=choosen)
        choosen.append(best)
        self.tournamentSelection2(tournamentsize = tournamentsize, numberToSelect = numberToSelect-1, choosen = choosen)


    def crossover(self):
        print("CROSSOVER")
        if self.crossover_probability == 0:
            self.choosen=[]
            #self.notChoosen=[]
            return
        #print ("Choosen/NotChoosen: {}/{}".format(len(self.choosen),len(self.notChoosen)))
        new_population=[]
        for i in self.choosen:
            x=random.uniform(0,1)
            if float(self.crossover_probability) < x:
                print ('TO CROSSOVER',x)
                self.pop.append(self.choosen.pop())
        #random.shuffle(self.choosen)
       # print("Choosen/NotChoosen: {}/{}".format(len(self.choosen), len(self.notChoosen)))
        counter=0
        len_choosen = len(self.choosen)
        while len(self.choosen)>2:
            #print("CROSSOVER")
            #print (counter)
            counter+=1
            try:
                ch1 = copy.deepcopy(self.choosen[counter])
                ch2 = copy.deepcopy(self.choosen[counter+1]) ## SPRAWDZIC
            except IndexError:
                if ch1:
                    new_population.append(ch1)
                    break
                else:
                    break
            counter+=1

            #print(counter)
            crossPoints = random.sample(range(1, self.route_size - 1), random.randint(0, self.route_size - 2))
            for i in crossPoints:
                status=1
                for y in ch1.route:
                    if y.idx == ch2.route[i].idx:
                        status=0
                if status == 1:
                    ch1.route[i] = ch2.route[i]
            new_population.append(ch1)
            new_population.append(ch2)
        #new_population.extend(self.choosen)
        #new_population.extend(self.notChoosen)
        #print ("choosen/notchoosen/population {}/{}/{}".format(len(self.choosen),len(self.notChoosen),len(new_population)))
        #print ("123123",self.pop)
        self.sortByFitness()
        #print("333323", self.pop)
        while self.populationSize>len(new_population):
           # print("choosen/notchoosen/population {}/{}/{}".format(len(self.choosen), len(self.notChoosen),
           #                                                       len(new_population)))
            try:
                xxx=self.choosen.pop()
            except IndexError:
                print ("koniec")
                self.pop = self.pop + new_population
                self.removeDuplicates()
                return
            new_population.append(xxx)

        self.pop = new_population

        #print("New Population: {}".format(len(new_population)))

