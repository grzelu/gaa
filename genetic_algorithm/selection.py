import random


class Selection(object):
    def __init__(self, population_class):
        self.population = population_class

    def selection__best_half(self, number_to_select=50):
        self.population.choosen = []
        self.population.sort_by_fitness()
        popsize = len(self.pop)
        for i in range(0, number_to_select):
            self.population.choosen.append(self.pop.pop(i))

    def random_select(self, number_to_select=50):
        self.population.choosen = []
        x = self.population.pop
        random.shuffle(x)
        for i in range(0, number_to_select):
            self.population.choosen.append(self.population.pop.pop())

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
            self.population.choosen = choosen
            self.population.pop = self.population.pop + self.population.choosen
            return self.population.choosen
        for i in range(0, tournament_size):
            member = self.population.pop[random.randint(0,len(self.population.pop)-1)]
            tournament_members.append(member)

        best,rest = self.trn_select(tournament_members)

        self.population.pop.remove(best)

        if best in self.population.pop:
            return
#           self.tournament_selection(tournament_size=tournament_size,
        # number_to_select=number_to_select, choosen=choosen)
        choosen.append(best)
        self.population.tournament_selection(tournament_size= tournament_size, number_to_select=number_to_select - 1, choosen = choosen)
