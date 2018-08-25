import copy, random


class Mutation(object):
    def __init__(self, population_class):
        self.population = population_class
        self.probability = self.population.mutation_probability
        self.mutation_variants = [self.swap_position, self.change_one, self.change_more]

    def swap_position(self):
        pass
    def change_one(self):
        pass
    def change_more(self):
        pass
    def mutation(self, mutation_options):

        mutate = []
        mutation_method = mutation_options
        for i in self.population.pop:
            rand = random.uniform(0 ,1)
            if rand < self.population.mutation_probability:
                method = random.choice(mutation_method)
                mutate.append({"route" :i, "method" :method})

        for i in mutate:
            if i['method'] == 'swapPosition':
                print("SWAP POSITION")
                to_swap = random.sample(range(1 ,len(i['route'].route ) -1) ,2)
                _cpy = copy.deepcopy(i['route'])
                i['route'].route[to_swap[0]] = _cpy.route[to_swap[1]]
                i['route'].route[to_swap[1]] = _cpy.route[to_swap[0]]
                i['route'].calc_fitness()
            elif i['method'] == 'changeOne':
                print("CHANGE ONE")
                to_change = random.randint(1 ,len(i['route'].route ) -1)
                __ch_list = copy.deepcopy(self.population.chromosome_list)
                ch_list = __ch_list[1:-1]
                random.shuffle(ch_list)
                for chr in ch_list:
                    is_valid = True

                    for y in range(1, len(i['route'].route ) -1):
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
                rang = range(1, len(i['route'].route ) -1)
                count = random.randint(1, len(i['route'].route ) -2)
                _to_change = random.sample(rang, count)
                __ch_list = copy.deepcopy(self.chromosome_list)
                ch_list = __ch_list[1:-1]
                random.shuffle(ch_list)

                for to_change in _to_change:
                    for chr in ch_list:
                        is_valid = True
                        for y in range(1, len(i['route'].route ) -1):
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
                _tab = list(range(1, len(i['route'].route ) -1))
                _2tab = list(range(1, len(i['route'].route ) -1))
                random.shuffle(_2tab)
                for c in _tab:
                    i['route'].route[c] = chrroute[c - 1]
                i['route'].calc_fitness()

    def _select_method(self):
        if random.uniform(0, 1) > self.probability:
            random.choice()