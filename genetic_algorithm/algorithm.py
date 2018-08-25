from population.population_class import Population
from gui_app.graph_manager import GraphManager
import numpy as np
import copy


class GeneticAlgorithmOptions(object):
    def __init__(self, arguments):
        self.tournament_size = arguments['tournament_size']
        self.tournament_select = arguments['tournament_select']
        self.elitism = arguments['elitism']
        self.crossover_options = arguments['crossoverOptions']
        self.mutation_options = arguments['mutationOptions']
        self.selection_options = arguments['selectOption']
        self.gui_graph = arguments['graph']
        self.gui_canvas = arguments['canvas']
        self.gui_windows = arguments['windows']


class GeneticAlgorithm(Population):
    def __init__(self, *args, **kwargs):
        super(GeneticAlgorithm, self).__init__(*args)
        self.options = GeneticAlgorithmOptions(kwargs)
        self.calc_fitness()
        self.the_best = None
        self.__fitness_scores = []
        self.__meanfitness_scores = []
        self.__worst_fitness_scores= []
        self.gui = GraphManager(self.options.gui_graph,
                                self.options.gui_canvas,
                                self.options.gui_windows)

    def make_population_label_text(self, first_generation=False):
        text = ""
        for i in self.pop:
            text = text + str(i) + "\n"
        return self.gui.windows.first_population.config(text=text) if first_generation \
            else self.gui.windows.current_population.config(text=text)

    def crossover(self):
        if self.options.crossover_options == "Random Points":
            self.crossover__random_points()
        elif self.options.crossover_options == "One Point of Crossing":
            self.crossover_pointOfCross()
        elif self.options.crossover_options == "Two Point of Crossing":
            self.crossover_two_pointsof_crossing()

    def selection(self):
        if self.options.selection_options == "Tournament Selection":
            self.tournament_selection(tournament_size=self.options.tournament_size,
                                      number_to_select=self.options.tournament_select,
                                      choosen=[])
        elif self.options.selection_options == "Random":
            self.random_select(number_to_select=self.options.tournament_select)
        elif self.options.selection_options == "Best":
            self.selection__best_half(number_to_select=self.options.tournament_select)

    def start_ga(self, n_iterations = 100):
        self.make_population_label_text(first_generation=True)

        for i in range(0, n_iterations):
            self.make_population_label_text()
            self.selection()
            self.crossover()
            self.mutation(self.options.mutation_options)
            self.calc_fitness()
            self.make_population_label_text()
            self.sort_by_fitness()

            fit = []
            if self.options.elitism == 1:
                self.sort_by_fitness()
                self.the_best = self.pop[0] if not self.the_best else self.pop.append(self.the_best)

            for y in self.pop:
                fit.append(round(y.fitness, 3))
            self.__meanfitness_scores.append(np.mean(fit))
            if len(self.options.gui_graph) > 0:
                self.graph(i)

    def draw_best(self, epoch):
        self.gui.graph.best_population.prepare()
        self.gui.graph.best_population.plot([i.x for i in self.chromosome_list], [i.y for i in self.chromosome_list], 'ro')
        best = self.pop[0]
        worst = self.pop[-1]
        for i in self.chromosome_list:
            self.gui.graph.best_population.annotate(i.name, xy=(i.x, i.y), xytext=(i.x, i.y))
        for i in range(0, len(self.the_best.route) - 1):
            self.gui.graph.best_population.plot([self.the_best.route[i].x, self.the_best.route[i + 1].x],
                                         [self.the_best.route[i].y, self.the_best.route[i + 1].y], 'g')
        self.gui.canvas.best_population.draw()

    def graph(self, counter=0):
        counter += 1
        self.sort_by_fitness()

        best = self.pop[0]
        worst = self.pop[-1]

        if not self.the_best:
            self.the_best = self.pop[0]
            self.draw_best(counter)
        try:
            if self.the_best.fitness > best.fitness:
                self.the_best = copy.deepcopy(self.pop[0])
                self.draw_best(counter)
        except IndexError:
            self.the_best = best

        self.__fitness_scores.append(best.fitness)
        self.__worst_fitness_scores.append(worst.fitness)
        self.gui.graph.current_population.prepare()
        self.gui.graph.best_fitness.prepare()
        self.gui.graph.best_fitness.plot(counter, self.__fitness_scores[-1], 'ro')
        self.gui.graph.best_fitness.plot(counter, self.__meanfitness_scores[-1], 'bo')
        self.gui.canvas.best_fitness.draw()

        _x = [i.x for i in self.chromosome_list]
        _y = [i.y for i in self.chromosome_list]

        self.gui.graph.current_population.plot(_x, _y, 'ro')
        for i in self.chromosome_list:
            self.gui.graph.current_population.annotate(i.name, xy=(i.x, i.y), xytext=(i.x, i.y))
        for i in range(0, len(best.route)-1):
            self.gui.graph.current_population.plot([best.route[i].x, best.route[i + 1].x],
                                                   [best.route[i].y, best.route[i + 1].y],
                                                   'g')
            self.gui.graph.current_population.plot([worst.route[i].x, worst.route[i + 1].x],
                                                   [worst.route[i].y, worst.route[i + 1].y],
                                                   'r')
            self.gui.canvas.current_population.draw()




