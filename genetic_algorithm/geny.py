import numpy as np
import random


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


