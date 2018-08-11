import numpy as np
import random
import copy
data_path = "vars/DANE.txt"
data_matrix = np.loadtxt(data_path, skiprows=25)
flow_matrix = data_matrix
data_file = open(data_path,'r')
city_list = []
flow_list = []
flow = False
counter = 0

while True:

    line = data_file.readline().strip('\r\n')
    if line == '---':
        data_file.close()
        break
    temp = line.split(' ')
    city_list.append({'idx':counter, 'name':temp[0],'x':temp[1],'y':temp[2]})
    counter += 1


class City():
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

    def distance_to(self, city):
        return np.sqrt(abs((city.x-self.x))^2+abs((city.y-self.y))^2)

    def speed_limit_to(self, city):
        return self.flow_matrix[self.idx][city.idx]


class Route:
    _counter = 1

    def __init__(self, route_size, chromosome_list, random_pop, counter):
        self.route = [chromosome_list[0]]
        self.route.extend(random.sample(chromosome_list[1:-1], route_size - 2))
        self.route.extend(chromosome_list[-1:])
        self.fitness = 0
        self.n_fitness = 0

    def calc_fitness(self):
        self.fitness = 0
        dist = 0
        total_time = 0
        v_max_all = 0
        for i in range(0, len(self.route)-1):
            dst = self.route[i].distance_to(self.route[i + 1]) * 1
            vmax = self.route[i].speed_limit_to(self.route[i + 1])
            dist = dist + dst
            v_max_all = v_max_all + vmax
            time = dst / vmax
            total_time = total_time + time

            self.fitness += time

        self.fitness = self.fitness*100

    def __str__(self):
        string = "F:{} ".format(round(self.fitness),2)
        for i in self.route:

            string = string + "[{}] ".format(i.idx)
        return string

    def __repr__(self):
        return self.__str__()


chromosome_list = [City(i, flow_matrix) for i in city_list]


class population(list):

    def __init__(self, chromosome_list, population_size, route_size, crossover_probability, mutation_probability, random_population = False):
        self.route_size = route_size
        self.counter=0
        self.population_size = population_size
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.chromosome_list = chromosome_list
        self.pop = []
        [self.pop.append(Route(route_size, chromosome_list, random_population, counter=self.counter)) for i in range(0, population_size)]

        self.selected=[]

    def calc_fitness(self):
        [i.calc_fitness() for i in self.pop]

    def remove_duplicates(self):
        lenpop = len(self.pop)
        x = self.pop
        xx = set(self.pop)
        lenset = len(xx)
        npop = []
        for i in xx:
            npop.append(i)
        self.pop= npop

    def normalize_fitness(self):
        all_fitness = 0
        n_fit = 0
        for i in self.pop:
            all_fitness += i.fitness

        for i in self.pop:
            i.n_fitness = i.fitness / all_fitness
        self.mean_fitness = all_fitness / len(self.pop)

    def sort_by_fitness(self):
        self.pop.sort(key=lambda x: x.fitness, reverse=False)

    def mutation(self, mutation_options):

        mutate = []
        mutation_method = mutation_options
        for i in self.pop:
            rand = random.uniform(0,1)
            if rand < self.mutation_probability:
                method = random.choice(mutation_method)
                mutate.append({"route":i, "method":method})

        for i in mutate:
            if i['method'] == 'swapPosition':
                print("SWAP POSITION")
                to_swap = random.sample(range(1,len(i['route'].route)-1),2)
                _cpy = copy.deepcopy(i['route'])
                i['route'].route[to_swap[0]] = _cpy.route[to_swap[1]]
                i['route'].route[to_swap[1]] = _cpy.route[to_swap[0]]
                i['route'].calc_fitness()
            elif i['method'] == 'changeOne':
                print("CHANGE ONE")
                to_change = random.randint(1,len(i['route'].route)-1)
                __ch_list = copy.deepcopy(self.chromosome_list)
                ch_list = __ch_list[1:-1]
                random.shuffle(ch_list)
                for chr in ch_list:
                    is_valid = True

                    for y in range(1, len(i['route'].route)-1):
                        if chr.idx == i['route'].route[y].idx:
                            is_valid = False
                    if is_valid:
                        if int(chr.idx) == 23:
                            continue
                        if int(i['route'].route[to_change].idx) == 23:
                            continue
                        i['route'].route[to_change] = chr
                        i['route'].calc_fitness()
                        break

            elif i['method'] == 'changeMore':
                rang = range(1, len(i['route'].route)-1)
                count = random.randint(1, len(i['route'].route)-2)
                _to_change = random.sample(rang, count)
                __ch_list = copy.deepcopy(self.chromosome_list)
                ch_list = __ch_list[1:-1]
                random.shuffle(ch_list)

                for to_change in _to_change:
                    for chr in ch_list:
                        is_valid = True
                        for y in range(1, len(i['route'].route)-1):
                            if chr.idx == i['route'].route[y].idx:
                                is_valid = False
                        if is_valid:
                            if int(chr.idx) == 23:
                                continue
                            if int(i['route'].route[to_change].idx) == 23:
                                continue
                            i['route'].route[to_change] = chr
                            i['route'].calc_fitness()
                            break

            elif i['method'] == 'shuffle':
                chr = copy.deepcopy(i['route'])
                chrroute = chr.route[1:-1]
                random.shuffle(chrroute)
                _tab = list(range(1, len(i['route'].route)-1))
                _2tab = list(range(1, len(i['route'].route)-1))
                random.shuffle(_2tab)
                for c in _tab:
                    i['route'].route[c] = chrroute[c - 1]
                i['route'].calc_fitness()

    def selection__best_half(self, number_to_select=50):
        self.choosen = []
        self.sort_by_fitness()
        popsize = len(self.pop)
        for i in range(0, number_to_select):
            self.choosen.append(self.pop.pop(i))

    def random_select(self, number_to_select=50):
        self.choosen = []
        x = self.pop
        random.shuffle(x)
        for i in range(0, number_to_select):
            self.choosen.append(self.pop.pop())

    def trn_select(self, tournament_members):
        best = None
        rest = []
        for i in tournament_members:
            if not best:
                best = i
            if i.fitness < best.fitness:
                best = i
            else:
                rest.append(i)
        return best, rest

    def tournament_selection(self, tournament_size=5, number_to_select=50, choosen=[]):
        tournament_members = []
        if number_to_select == 0:
            self.choosen = choosen
            self.pop = self.pop + self.choosen
            return self.choosen
        for i in range(0, tournament_size):
            member = self.pop[random.randint(0,len(self.pop)-1)]
            tournament_members.append(member)

        best,rest = self.trn_select(tournament_members)

        self.pop.remove(best)

        if best in self.pop:
            return
#           self.tournament_selection(tournament_size=tournament_size,
        # number_to_select=number_to_select, choosen=choosen)
        choosen.append(best)
        self.tournament_selection(tournament_size= tournament_size, number_to_select=number_to_select - 1, choosen = choosen)

    def crossover__random_points(self):
        if self.crossover_probability == 0:
            self.choosen = []
            return
        new_population = []
        for i in self.choosen:
            x = random.uniform(0, 1)
            if float(self.crossover_probability) < x:
                new_population.append(self.choosen.pop())
        counter = 0
        while len(self.choosen) > 2:
            try:
                ch1 = copy.deepcopy(self.choosen[counter])
                ch2 = copy.deepcopy(self.choosen[counter+1])
            except IndexError:
                if ch1:
                    break
                else:
                    break
            counter += 2

            cross_points = random.sample(range(1, self.route_size - 1), random.randint(0, self.route_size - 2))
            for i in cross_points:
                status = 1
                for y in ch1.route:
                    if y.idx == ch2.route[i].idx:
                        status = 0
                if status == 1:
                    ch1.route[i] = ch2.route[i]
            ch1.calc_fitness()

            new_population.append(ch1)
        self.pop.extend(new_population)
        self.pop.extend(self.choosen)
        self.sort_by_fitness()
        self.remove_duplicates()
        self.pop = self.pop[:self.population_size]

    def crossover_two_pointsof_crossing(self):
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
            ch1.calc_fitness()

            new_population.append(ch1)
        self.pop.extend(new_population)
        self.pop.extend(self.choosen)
        self.sort_by_fitness()
        #self.removeDuplicates()
        self.pop = self.pop[:self.population_size]

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
            ch1.calc_fitness()

            new_population.append(ch1)
        self.pop.extend(new_population)
        self.pop.extend(self.choosen)
        self.sort_by_fitness()
        self.remove_duplicates()
        self.pop = self.pop[:self.population_size]


