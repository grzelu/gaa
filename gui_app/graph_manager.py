from abc import ABCMeta


class GraphManager:
    def __init__(self, graphs, canvas, windows):
        self.graph = Graphs(graphs)
        self.canvas = Canvas(canvas)
        self.windows = Window(windows)


class Graphs:
    def __init__(self, graphs):
        self.current_population = CurrentPopulationGraph(graphs[0])
        self.best_population = BestPopulationGraph(graphs[1])
        self.best_fitness = BestFitnessGraph(graphs[2])


class PersonalizedGraph:
    __metaclass__ = ABCMeta

    def __init__(self, graph):
        self.graph = graph
        self.prepare()

    def plot(self, *args, **kwargs):
        self.graph.plot(*args, **kwargs)

    def annotate(self, *args, **kwargs):
        self.graph.annotate(*args, **kwargs)

    def prepare(self):
        self._set_common_settings()

    def _set_common_settings(self):
        self.graph.clear()
        self.graph.grid(True, alpha=0.2, linewidth=1, pickradius=5)
        self.graph.set_ylabel("Y")
        self.graph.set_xlabel("X")


class CurrentPopulationGraph(PersonalizedGraph):
    def prepare(self):
        self._set_common_settings()
        self.graph.set_title('Current population BEST(g)/WORST(r)')
        self.graph.legend(['City', 'Best route', 'Worst route'])


class BestPopulationGraph(PersonalizedGraph):
    def prepare(self):
        self._set_common_settings()
        self.graph.set_title('Best population BEST(g)/WORST(r)')
        self.graph.legend(['City', 'Best route', 'Worst route'])


class BestFitnessGraph(PersonalizedGraph):
    def prepare(self):
        self.graph.set_title('Fitness')
        self.graph.set_xlabel("Epoch")
        self.graph.set_ylabel("Fitness")
        self.graph.grid(True, alpha=0.2, linewidth=1, pickradius=5)
        self.graph.legend(['Best score', 'Mean score'])


class Canvas:
    def __init__(self, canvas):
        self.current_population = canvas[0]
        self.best_population = canvas[1]
        self.best_fitness = canvas[2]
        pass


class Window:
    def __init__(self, windows):
        self.current_population = windows[0]
        self.first_population = windows[1]
        pass
