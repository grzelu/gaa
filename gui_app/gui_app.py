import matplotlib, time, random, threading, sys
from genetic_algorithm.algorithm import GeneticAlgorithm
from vars.var import chromosome_list


matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk


class GuiApp():
    def __init__(self):
        self.root = Tk.Tk()
        self.root.geometry("1466x900")
        self.root.wm_title("Genetic Algorithm - SWDiSK 2018 [PWR]")
        self.create_frames()
        self.create_options()
        self.create_enties()
        self.create_figures()
        self.create_check_buttons()
        self.create_labels()
        self.create_buttons(self.framebuttons)
        self.randomPopulation = True
        self.elitism = 0
        self.startCounter = 0

    def create_options(self):
        label = Tk.Label(self.framebuttons, text="Selection options")
        label.pack(side=Tk.TOP,anchor='w')
        self._select_option_var = Tk.StringVar(self.framebuttons)
        self._select_option_var.set("Tournament Selection")
        w = Tk.OptionMenu(self.framebuttons, self._select_option_var, "Tournament Selection", "Random", "Best")
        w.pack(side=Tk.TOP,anchor='w')
        label = Tk.Label(self.framebuttons, text="Crossover options")
        label.pack(side=Tk.TOP,anchor='w')
        self.__crossover_option_var = Tk.StringVar(self.framebuttons)
        self.__crossover_option_var.set("Random Points")

        w = Tk.OptionMenu(self.framebuttons, self.__crossover_option_var, "Random Points", "One Point of Crossing", "Two Point of Crossing")
        w.pack(side=Tk.TOP,anchor='w')

    def create_frames(self):
        self._frame = Tk.Frame(self.root, bg='red')
        self._frame.pack(side=Tk.LEFT, anchor='nw')

        self.frame0 = Tk.Frame(self._frame, width=450, height=600, pady=3)
        self.frame0.pack(side=Tk.TOP, fill=Tk.Y)

        self.frame01 = Tk.Frame(self._frame,width=450, height=600, pady=3)
        self.frame01.pack(side=Tk.BOTTOM, fill=Tk.Y)

        self.framebuttons = Tk.Frame(self.root,width=200, height=300, pady=3)
        self.framebuttons.pack(side=Tk.LEFT, fill=Tk.Y)

        self.frame = Tk.Frame(self.root, width=450, height=600, pady=3)
        self.frame.pack(side=Tk.LEFT)

    def create_labels(self):
        #self.window = Tk.Toplevel(self.framebuttons)
        self.label_window_population = Tk.Label(self.frame, text='', fg='blue')
        self.label_window_population.pack(side=Tk.LEFT)

        self.label_window_first_population = Tk.Label(self.frame, text='', fg='red')
        self.label_window_first_population.pack(side=Tk.LEFT)

    def create_check_buttons(self):
        self.var = Tk.IntVar()
        label = Tk.Label(self.framebuttons, text="Mutation options")
        label.pack(side=Tk.TOP,anchor='w')
        self.generate_random = Tk.Checkbutton(self.framebuttons, text="Generate static", variable=self.var, command=self.cb)

        self.generate_random.pack(side=Tk.TOP, anchor='w')
        self._var_elitism = Tk.IntVar()
        elitism = Tk.Checkbutton(self.framebuttons, text="Elitism", variable=self._var_elitism, command=self.cb)
        elitism.select()
        elitism.pack(side=Tk.TOP,anchor='w')

        self._var_mutation_swap_position = Tk.IntVar()
        swapPosition = Tk.Checkbutton(self.framebuttons, text="swapPosition", variable=self._var_mutation_swap_position, command=self.cb)
        swapPosition.pack(side=Tk.TOP,anchor='w')

        self._var_mutation_change_one = Tk.IntVar()
        changeOne = Tk.Checkbutton(self.framebuttons, text="changeOne", variable=self._var_mutation_change_one, command=self.cb)
        changeOne.pack(side=Tk.TOP,anchor='w')

        self._var_mutation_shuffle = Tk.IntVar()
        shuffle = Tk.Checkbutton(self.framebuttons, text="shuffle", variable=self._var_mutation_shuffle, command=self.cb)
        shuffle.pack(side=Tk.TOP,anchor='w')
        shuffle.select()
        self._var_mutation_changeMore = Tk.IntVar()
        changeMore = Tk.Checkbutton(self.framebuttons, text="changeMore", variable=self._var_mutation_changeMore, command=self.cb)
        changeMore.pack(side=Tk.TOP,anchor='w')

    def get_mutation_methods(self):
        change_one = self._var_mutation_change_one.get()
        swap_position = self._var_mutation_swap_position.get()
        shuffle = self._var_mutation_shuffle.get()
        changeMore = self._var_mutation_changeMore.get()
        options = []
        if changeMore == 1:
            options.append("changeMore")
        if shuffle == 1:
            options.append("shuffle")
        if change_one == 1:
            options.append("change_one")
        if swap_position == 1:
            options.append("swap_position")
        return options

    def cb(self):
        self.randomPopulation = self.var.get()
        self.elitism = self._var_elitism.get()

    def create_enties(self):
        self.__crossover_probability_entry = self.make_entry(4, 7, 0.9, "Crossover probability")
        self.__mutation_probability_entry = self.make_entry(5, 7, 0.1, "Mutation probability")
        self.__tournamen_selection_size = self.make_entry(8, 7, 6, "size of tournament")
        self.__tournamen_selection_select = self.make_entry(9, 7, 60, "amount of selections")
        self.__pop_size_entry = self.make_entry(2, 7, 200, "Population size")
        self.__route_size_entry = self.make_entry(3, 7, 6, "Route size")
        self.__iterations = self.make_entry(6, 7, 200, "Iterations")
        self.__instantions = self.make_entry(7, 7, 1, "number of runs")

    def create_figures(self):
        self.left_figure = Figure(figsize=(7, 7), dpi=60)
        self.left_subplot = self.create_subplot(self.left_figure, "Current population BEST(g)/WORST(r)")
        self.left_canvas = self.create_canvas(self.left_figure, self.frame0, 'LEFT')

        self.right_figure = Figure(figsize=(7, 7), dpi=60)
        self.right_canvas = self.create_canvas(self.right_figure, self.frame0, 'RIGHT')
        self.right_subplot = self.create_subplot(self.right_figure, "Best solution so far")

        self.bot_left_figure = Figure(figsize=(14, 7), dpi=60)
        self.down_left_subplot = self.create_subplot(self.bot_left_figure, "Fitness")
        self.down_left_canvas = self.create_canvas(self.bot_left_figure, self.frame01, 'TOP')

#       self.botRightFigure = Figure(figsize=(7, 7), dpi=60)
#       self.downRightSubplot = self.createSubplot(self.botRightFigure, "Best of current generation")
#       self.downRightCanvas = self.createCanvas(self.botRightFigure, self.frame01, 'BOTTOM')

    def create_canvas(self, figure, master, side):
        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()

        if side == 'LEFT':
            canvas.get_tk_widget().pack(side=Tk.LEFT,anchor='nw')
        elif side == 'RIGHT':
            canvas.get_tk_widget().pack(side=Tk.LEFT,anchor='ne')
            canvas._tkcanvas.pack(side=Tk.LEFT,anchor='ne')
        elif side == 'TOP':
            canvas.get_tk_widget().pack(side=Tk.RIGHT,fill=Tk.X)
            canvas._tkcanvas.pack(side=Tk.RIGHT,fill=Tk.X)
        elif side == 'BOTTOM':
            canvas.get_tk_widget().pack(side=Tk.RIGHT)
            canvas._tkcanvas.pack(side=Tk.RIGHT)
        return canvas

    def make_entry(self, row, column, value, text):
        row = Tk.Frame(self.framebuttons)
        row.pack(side=Tk.TOP, fill=Tk.X)
        label = Tk.Label(row, text=text)
        entry = Tk.Entry(row)
        entry.pack(side=Tk.LEFT)
        label.pack(side=Tk.LEFT)
        entry.insert(0, value)
        return entry

    def create_subplot(self, figure, title, axes=[0, 800, 0, 800], ax = False):
        subplot = figure.add_subplot(111)
        subplot.set_title(title)
        subplot.set_xlabel('X')
        subplot.set_ylabel('Y')
        subplot.grid(True)
        if ax:
            subplot.set_xticks(np.arange(axes[0], axes[1], 100))
            subplot.set_yticks(np.arange(axes[2], axes[3], 100))
        return subplot

    def create_buttons(self, master):
        row = Tk.Frame(master)
        row.pack(side=Tk.TOP, fill=Tk.X)
        button = Tk.Button(master=row, text='Start', command=self.start)
        button.pack(side=Tk.LEFT)
        button2 = Tk.Button(master=row, text='Quit', command=self.quit)
        button2.pack(side=Tk.LEFT)
        button3 = Tk.Button(master=row, text='test', command=self.quit)
        button3.pack(side=Tk.LEFT)

    def run(self):
        Tk.mainloop()

    def start(self):
        self.startCounter +=1
        crossover_probability = float(self.__crossover_probability_entry.get())
        mutation_probability = float(self.__mutation_probability_entry.get())
        population_size = int(self.__pop_size_entry.get())
        route_size = int(self.__route_size_entry.get())
        tournament_size = int(self.__tournamen_selection_size.get())
        tournament_select = int(self.__tournamen_selection_select.get())
        select_option = self._select_option_var.get()
        mutation_options = self.get_mutation_methods()
        crossover_options = self.__crossover_option_var.get()
        self._GA = GeneticAlgorithm(chromosome_list, population_size, route_size, crossover_probability, mutation_probability,
                                    graph=[self.left_subplot, self.right_subplot, self.down_left_subplot],
                                    canvas=[self.left_canvas, self.right_canvas, self.down_left_canvas, ],
                                    windows=[self.label_window_population, self.label_window_first_population],
                                    tournament_size = tournament_size,
                                    tournament_select = tournament_select,
                                    elitism = self.elitism,
                                    selectOption=select_option,
                                    mutationOptions=mutation_options, startCounter=self.startCounter, crossoverOptions=crossover_options

                                    )

        self.new_thread = threading.Thread(target=self.update_graph, args=(self._GA,))
        self.new_thread.start()

    def update_graph(self, thr):
        thr.start_ga(n_iterations=int(self.__iterations.get()))

    def quit(self):
        self.root.destroy()
        sys.exit()
        pass
