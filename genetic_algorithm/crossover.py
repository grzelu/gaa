import random, copy


class Crossover(object):
    def __init__(self, population_class):
        self.population = population_class

    def random_points(self):
        if self.population.crossover_probability == 0:
            self.population.choosen = []
            return
        new_population = []
        for i in self.population.choosen:
            x = random.uniform(0, 1)
            if float(self.population.crossover_probability) < x:
                new_population.append(self.population.choosen.pop())
        counter = 0
        while len(self.population.choosen) > 2:
            try:
                ch1 = copy.deepcopy(self.population.choosen[counter])
                ch2 = copy.deepcopy(self.population.choosen[counter+1])
            except IndexError:
                if ch1:
                    break
                else:
                    break
            counter += 2

            cross_points = random.sample(range(1, self.population.route_size - 1), random.randint(0, self.population.route_size - 2))
            for i in cross_points:
                status = 1
                for y in ch1.route:
                    if y.idx == ch2.route[i].idx:
                        status = 0
                if status == 1:
                    ch1.route[i] = ch2.route[i]
            ch1.calc_fitness()

            new_population.append(ch1)
        self.population.pop.extend(new_population)
        self.population.pop.extend(self.population.choosen)
        self.population.sort_by_fitness()
        self.population.remove_duplicates()
        self.population.pop = self.population.pop[:self.population.population_size]

    def two_points(self):
        if self.population.crossover_probability == 0:
            self.population.choosen=[]
            return
        new_population=[]
        for i in self.population.choosen:
            x=random.uniform(0,1)
            if float(self.population.crossover_probability) < x:
                new_population.append(self.population.choosen.pop())
        counter=0
        while len(self.population.choosen)>2:
            try:
                ch1 = copy.deepcopy(self.population.choosen[counter])
                ch2 = copy.deepcopy(self.population.choosen[counter+1])
            except IndexError:
                if ch1:
                    break
                else:
                    break
            counter+=2
            left = random.randint(1, self.population.route_size-2)
            right = random.randint(left, self.population.route_size-1)

            crossPoints = list(range(left, right))
            for i in crossPoints:
                status=1
                for y in ch1.route:
                    if y.idx == ch2.route[i].idx:
                        status=0
                if status == 1:
                    ch1.route[i] = ch2.route[i]
            ch1.calc_fitness()

            new_population.append(ch1)
            self.population.pop.extend(new_population)
        self.population.pop.extend(self.population.choosen)
        self.population.sort_by_fitness()
        #self.removeDuplicates()
        self.population.pop = self.population.pop[:self.population.population_size]

    def one_point(self):
        if self.population.crossover_probability == 0:
            self.population.choosen=[]
            return
        new_population=[]
        for i in self.population.choosen:
            x=random.uniform(0,1)
            if float(self.population.crossover_probability) < x:
                new_population.append(self.population.choosen.pop())
        counter=0
        while len(self.population.choosen)>2:
            try:
                ch1 = copy.deepcopy(self.choosen[counter])
                ch2 = copy.deepcopy(self.choosen[counter+1])
            except IndexError:
                if ch1:
                    break
                else:
                    break
            counter+=2

            crossPoints = range(1,random.randint(1,self.population.route_size-1))
            for i in crossPoints:
                status=1
                for y in ch1.route:
                    if y.idx == ch2.route[i].idx:
                        status=0
                if status == 1:
                    ch1.route[i] = ch2.route[i]
            ch1.calc_fitness()

            new_population.append(ch1)
        self.population.pop.extend(new_population)
        self.population.pop.extend(self.population.choosen)
        self.population.sort_by_fitness()
        self.population.remove_duplicates()
        self.population.pop = self.population.pop[:self.population.population_size]