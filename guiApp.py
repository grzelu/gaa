import matplotlib, time, random, threading, sys
from ga import GA
from variables import *
from queue import Queue

matplotlib.use('TkAgg')
import copy

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from multiprocessing.pool import ThreadPool
import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk


class guiApp():
    def __init__(self):
        self.root = Tk.Tk()
        self.root.geometry("1466x900")
        self.root.wm_title("Genetic Algorithm - SWDiSK 2018 [PWR]")
        self.createFrames()
        self.createOptions()
        self.createEnties()
        self.createFigures()
        self.createCheckButtons()
        self.createLabels()
        self.createButtons(self.framebuttons)
        self.randomPopulation = True
        self.elitism = 0
        self.startCounter = 0

    def createOptions(self):
        label = Tk.Label(self.framebuttons, text="Selection options")
        label.pack(side=Tk.TOP,anchor='w')
        self._selectOptionVar = Tk.StringVar(self.framebuttons)
        self._selectOptionVar.set("Tournament Selection")
        w = Tk.OptionMenu(self.framebuttons,self._selectOptionVar, "Tournament Selection", "Random","Best")
        w.pack(side=Tk.TOP,anchor='w')
        label = Tk.Label(self.framebuttons, text="Crossover options")
        label.pack(side=Tk.TOP,anchor='w')
        self._CrossoverOptionVar = Tk.StringVar(self.framebuttons)
        self._CrossoverOptionVar.set("Random Points")

        w = Tk.OptionMenu(self.framebuttons,self._CrossoverOptionVar, "Random Points", "One Point of Crossing","Two Point of Crossing")
        w.pack(side=Tk.TOP,anchor='w')
    def createFrames(self):
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

    def createLabels(self):
        #self.window = Tk.Toplevel(self.framebuttons)
        self.LabelWindowPopulation = Tk.Label(self.frame, text='', fg='blue')
        self.LabelWindowPopulation.pack(side=Tk.LEFT)

        self.LabelWindowFirstPopulation = Tk.Label(self.frame, text='', fg='red')
        self.LabelWindowFirstPopulation.pack(side=Tk.LEFT)

    def createCheckButtons(self):
        self.var = Tk.IntVar()
        label = Tk.Label(self.framebuttons, text="Mutation options")
        label.pack(side=Tk.TOP,anchor='w')
        self.generateRandom = Tk.Checkbutton(self.framebuttons, text="Generate static", variable=self.var, command=self.cb)

        self.generateRandom.pack(side=Tk.TOP,anchor='w')
        self._var_elitism = Tk.IntVar()
        elitism = Tk.Checkbutton(self.framebuttons, text="Elitism", variable=self._var_elitism, command=self.cb)
        elitism.select()
        elitism.pack(side=Tk.TOP,anchor='w')

        self._var_mutation_swapPosition = Tk.IntVar()
        swapPosition = Tk.Checkbutton(self.framebuttons, text="swapPosition", variable=self._var_mutation_swapPosition, command=self.cb)
        swapPosition.pack(side=Tk.TOP,anchor='w')

        self._var_mutation_changeOne = Tk.IntVar()
        changeOne = Tk.Checkbutton(self.framebuttons, text="changeOne", variable=self._var_mutation_changeOne, command=self.cb)
        changeOne.pack(side=Tk.TOP,anchor='w')

        self._var_mutation_shuffle = Tk.IntVar()
        shuffle = Tk.Checkbutton(self.framebuttons, text="shuffle", variable=self._var_mutation_shuffle, command=self.cb)
        shuffle.pack(side=Tk.TOP,anchor='w')
        shuffle.select()
        self._var_mutation_changeMore = Tk.IntVar()
        changeMore = Tk.Checkbutton(self.framebuttons, text="changeMore", variable=self._var_mutation_changeMore, command=self.cb)
        changeMore.pack(side=Tk.TOP,anchor='w')

    def getMutationMethods(self):
        changeOne = self._var_mutation_changeOne.get()
        swapPosition = self._var_mutation_swapPosition.get()
        shuffle = self._var_mutation_shuffle.get()
        changeMore = self._var_mutation_changeMore.get()
        options = []
        if changeMore == 1:
            options.append("changeMore")
        if shuffle == 1:
            options.append("shuffle")
        if changeOne == 1:
            options.append("changeOne")
        if swapPosition == 1:
            options.append("swapPosition")
        return options

    def cb(self):
        self.randomPopulation = self.var.get()
        self.elitism = self._var_elitism.get()

    def createEnties(self):
        self.__crossoverProbabilityEntry = self.makeEntry(4, 7, 0.9, "Crossover probability")
        self.__mutationProbabilityEntry = self.makeEntry(5, 7, 0.1, "Mutation probability")
        self.__tournamenSelectionSize = self.makeEntry(8, 7, 6, "size of tournament")
        self.__tournamenSelectionSelect = self.makeEntry(9,7, 60, "amount of selections")
        self.__popSizeEntry = self.makeEntry(2, 7, 200, "Population size")
        self.__routeSizeEntry = self.makeEntry(3, 7, 6, "Route size")
        self.__iterations = self.makeEntry(6, 7, 200, "Iterations")
        self.__instantions = self.makeEntry(7, 7, 1, "number of runs")

    def createFigures(self):
        self.leftFigure = Figure(figsize=(7, 7), dpi=60)
        self.leftSubplot = self.createSubplot(self.leftFigure, "Current population BEST(g)/WORST(r)")
        self.leftCanvas = self.createCanvas(self.leftFigure, self.frame0, 'LEFT')

        self.rightFigure = Figure(figsize=(7, 7), dpi=60)
        self.rightCanvas = self.createCanvas(self.rightFigure, self.frame0, 'RIGHT')
        self.rightSubplot = self.createSubplot(self.rightFigure, "Best solution so far")

        self.botLeftFigure = Figure(figsize=(14, 7), dpi=60)
        self.downLeftSubplot = self.createSubplot(self.botLeftFigure, "Fitness")
        self.downLeftCanvas = self.createCanvas(self.botLeftFigure, self.frame01, 'TOP')

        #self.botRightFigure = Figure(figsize=(7, 7), dpi=60)
        #self.downRightSubplot = self.createSubplot(self.botRightFigure, "Best of current generation")
        #self.downRightCanvas = self.createCanvas(self.botRightFigure, self.frame01, 'BOTTOM')

    def createCanvas(self, figure, master, side):
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

    def makeEntry(self, row, column, value, text):
        row = Tk.Frame(self.framebuttons)
        row.pack(side=Tk.TOP, fill=Tk.X)
        label = Tk.Label(row, text=text)
        entry = Tk.Entry(row)
        entry.pack(side=Tk.LEFT)
        label.pack(side=Tk.LEFT)
        entry.insert(0, value)
        return entry

    def createSubplot(self, figure, title, axes=[0, 800, 0, 800],ax = False):
        subplot = figure.add_subplot(111)
        subplot.set_title(title)
        subplot.set_xlabel('X')
        subplot.set_ylabel('Y')
        subplot.grid(True)
        if ax:
            subplot.set_xticks(np.arange(axes[0], axes[1], 100))
            subplot.set_yticks(np.arange(axes[2], axes[3], 100))
        return subplot

    def createButtons(self, master):
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
        crossover_probability = float(self.__crossoverProbabilityEntry.get())
        mutation_probability = float(self.__mutationProbabilityEntry.get())
        population_size = int(self.__popSizeEntry.get())
        route_size = int(self.__routeSizeEntry.get())
        tournament_size = int(self.__tournamenSelectionSize.get())
        tournament_select = int(self.__tournamenSelectionSelect.get())
        selectOption = self._selectOptionVar.get()
        mutationOptions = self.getMutationMethods()
        crossoverOptions = self._CrossoverOptionVar.get()
        self._GA = GA(chromosome_list, population_size, route_size, crossover_probability, mutation_probability,
                      test="TEST",
                      randomPopulation=self.randomPopulation,
                      graph=[self.leftSubplot, self.rightSubplot, self.downLeftSubplot],
                      canvas=[self.leftCanvas, self.rightCanvas,  self.downLeftCanvas, ],
                      windows=[self.LabelWindowPopulation, self.LabelWindowFirstPopulation],
                      tournament_size = tournament_size,
                      tournament_select = tournament_select,
                      elitism = self.elitism,
                      selectOption=selectOption,
                      mutationOptions=mutationOptions,startCounter=self.startCounter,crossoverOptions=crossoverOptions

                      )

        threads = 0
        for i in range(0, int(self.__instantions.get()) - 1):
            x = GA(chromosome_list, population_size, route_size, crossover_probability, mutation_probability,
                   randomPopulation=self.randomPopulation,
                   graph=[self.leftSubplot, self.rightSubplot, self.downRightSubplot, self.downLeftSubplot],
                   canvas=[self.leftCanvas, self.rightCanvas, self.downRightCanvas, self.downLeftCanvas],
                   windows=[self.LabelWindowPopulation, self.LabelWindowFirstPopulation],
                   tournament_size = tournament_size,
                   tournament_select = tournament_select,
                   elitism = self.elitism,
                   selectOption=selectOption,
                   mutationOptions=mutationOptions,crossoverOptions=crossoverOptions
                   )

            self.i = threading.Thread(target=self.updateGraph, args=(x,))
            threads += 1
            self.i.start()
        self.new_thread = threading.Thread(target=self.updateGraph, args=(self._GA,))
        self.new_thread.start()
        print("Number of threads: {}".format(threads))

    def updateGraph(self, thr):
        thr.startGA(n_iterations=int(self.__iterations.get()))

    def quit(self):
        self.root.destroy()
        sys.exit()
        pass
