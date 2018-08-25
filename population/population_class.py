from genetic_algorithm.geny import Route
from genetic_algorithm.selection import Selection
from genetic_algorithm.mutation import Mutation
from genetic_algorithm.crossover import Crossover


class Population(list):

    def __init__(self, chromosome_list, population_size, route_size, crossover_probability, mutation_probability, random_population = False):
        self.route_size = route_size
        self.counter=0
        self.population_size = population_size
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.chromosome_list = chromosome_list
        self.pop = []
        [self.pop.append(Route(route_size, chromosome_list, random_population, counter=self.counter)) for i in range(0, population_size)]

        self.selected = []
        self._selection = Selection(self)
        self._mutation = Mutation(self)
        self._crossover = Crossover(self)


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

        self._mutation.mutation(mutation_options)

    def selection__best_half(self, number_to_select=50):
        self._selection.best_half(number_to_select)

    def random_select(self, number_to_select=50):
        self._selection.random_select(number_to_select)

    def trn_select(self, tournament_members):
        self._selection.trn_select(tournament_members)

    def tournament_selection(self, tournament_size=5, number_to_select=50, choosen=[]):
        self._selection.tournament_selection(tournament_size, number_to_select, choosen)

    def crossover__random_points(self):
        self._crossover.random_points()

    def crossover_two_pointsof_crossing(self):
        self._crossover.two_points()

    def crossover_pointOfCross(self):
        self._crossover.one_point()