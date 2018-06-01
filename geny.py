import numpy as np
import random
import copy
data_path = "DANE.txt"
data_matrix = np.loadtxt(data_path,skiprows=13)
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
    def __init__(self, routeSize,chromosome_list):
        self.route = [chromosome_list[0]]
        self.route.extend(random.sample(chromosome_list[1:-1], routeSize-2))
        self.route.extend(chromosome_list[-1:])
        self.fitness = 0
        self.n_fitness = 0

    def calcFitness(self):
        self.fitness=0;
        for i in range(0,len(self.route)-1):
            dst = self.route[i].distanceTo(self.route[i+1])
            vmax = self.route[i].speedLimitTo(self.route[i+1])
            time = dst/vmax
            #print ("Time: {} = Dist: {} / Speed: {}".format(time,dst,vmax))
            self.fitness+=time

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
    def __init__(self,chromosome_list, populationSize, route_size,crossover_probability, mutation_probability):
        self.route_size=route_size
        self.populationSize = populationSize
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.chromosome_list = chromosome_list
        self.pop=[]
        [self.pop.append(route(route_size, chromosome_list)) for i in range(0, populationSize)]
        self.selected=[]
    def calcFitness(self):
        [i.calcFitness() for i in self.pop]
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
        mutation_method = ['swapPosition', 'changeOne']
        #mutation_method = ['swapPosition','changeOne','changeMore']
        #mutation_method = ['changeMore']
        for i in self.pop:
            rand = random.uniform(0,1)
            if rand < self.mutation_probability:
                method = random.choice(mutation_method)
                print ('mutuje',i,self.mutation_probability, method, rand)
                mutate.append({"route":i, "method":method})
        for i in mutate:
            if i['method'] == 'swapPosition':
                toSwap = random.sample(range(1,len(i['route'].route)-1),2)
                print (toSwap)
                _cpy = copy.deepcopy(i['route'])
                #print (i['route'].route)
                i['route'].route[toSwap[0]] = _cpy.route[toSwap[1]]
                i['route'].route[toSwap[1]] = _cpy.route[toSwap[0]]
                #print(i['route'].route)
            elif i['method'] == 'changeOne':
                toChange = random.randint(1,len(i['route'].route)-1)
                ch_list = copy.deepcopy(self.chromosome_list)
                random.shuffle(ch_list)
                print (i['route'].route)
                for chr in ch_list:
                    isValid = True
                    for y in range(1,len(i['route'].route)-1):
                        if chr==i['route'].route[y]:
                            isValid= False
                    if isValid == True:
                        i['route'].route[toChange] = chr
                        break

            elif i['method'] == 'changeMore':
                amountToChange = random.randint(1, len(i['route'].route) - 1)
                #valuesToChange = random.sample(range(1,len(i['route'].route) - 1),amountToChange)
                #print (valuesToChange)


    def tournamentSelection(self):
        #temp  = copy.deepcopy(self.pop)
        self.notChoosen=[]
        random.shuffle(temp)
        self.choosen = []
        final = []
        while len(self.pop)>1:
            ch1 = self.pop.pop()
            ch2 = self.pop.pop()
            if ch1.fitness < ch2.fitness:
                self.choosen.append(ch1)
                self.notChoosen.append(ch2)
            else:
                self.choosen.append(ch2)
                self.notChoosen.append(ch1)
        #while len(choosen)>1:
        #    ch1 = choosen.pop()
        #    ch2 = choosen.pop()
        #    if ch1.fitness < ch2.fitness:
        #        final.append(ch1)
        #    else:
        #        final.append(ch2)
        #print (final,len(final))
        self.notChoosen.sort(key=lambda x: x.fitness, reverse=False)
        return self.choosen

    def crossover(self):
        #print ("Choosen/NotChoosen: {}/{}".format(len(self.choosen),len(self.notChoosen)))
        new_population=[]
        for i in self.choosen:
            if self.mutation_probability > random.uniform(0,1):
                self.notChoosen.append(self.choosen.pop())
        random.shuffle(self.choosen)
        #print("Choosen/NotChoosen: {}/{}".format(len(self.choosen), len(self.notChoosen)))
        counter=0
        len_choosen = len(self.choosen)
        while len(self.choosen)>2:
            #print (counter)
            counter+=1
            try:
                ch1 = copy.deepcopy(self.choosen[counter])
                ch2 = copy.deepcopy(self.choosen[counter])
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
       # print ("choosen/notchoosen/population {}/{}/{}".format(len(self.choosen),len(self.notChoosen),len(new_population)))
        while self.populationSize>len(new_population):
           # print("choosen/notchoosen/population {}/{}/{}".format(len(self.choosen), len(self.notChoosen),
           #                                                       len(new_population)))
            try:
                new_population.append(self.notChoosen.pop())
            except IndexError:
                new_population.append(self.choosen.pop())
        self.pop = new_population
        #print("New Population: {}".format(len(new_population)))

