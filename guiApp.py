import matplotlib, time, random, threading, sys
from ga import GA
from variables import *
from queue import Queue

matplotlib.use('TkAgg')
import copy

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk


class guiApp():
    def __init__(self):
        self.root = Tk.Tk()
        self.root.geometry("1466x700")
        self.root.wm_title("Genetic Algorythm")
        #self.root.pack_slaves()
        self._frame = Tk.Frame(self.root, bg='red')
        self._frame.pack(side = Tk.LEFT,anchor='nw')
        self.frame0 = Tk.Frame(self._frame, bg='blue', width=450, height=600, pady=3)
        self.frame0.pack(side=Tk.TOP, fill=Tk.Y)
        self.frame01 = Tk.Frame(self._frame, bg='green', width=450, height=600, pady=3)
        self.frame01.pack(side=Tk.BOTTOM, fill=Tk.Y)

        self.framebuttons = Tk.Frame(self.root, bg='yellow', width=200, height=300, pady=3)
        self.framebuttons.pack(side=Tk.LEFT,fill=Tk.Y)

        self.frame = Tk.Frame(self.root, bg='cyan', width=450, height=600, pady=3)
        self.frame.pack(side=Tk.LEFT)


        #self.frame.grid(column=10, row=0, sticky="ew", rowspan=10)
        #self.root.grid_rowconfigure(1, weight=1)

        self.createButtons(self.framebuttons)

        self.createEnties()
        self.createFigures()

        #self.window = Tk.Toplevel(self.framebuttons)
        self.LabelWindowPopulation = Tk.Label(self.frame, text='', fg='blue')
        self.LabelWindowPopulation.pack(side=Tk.LEFT)
        #self.LabelWindowPopulation.grid(row=0, column=0, rowspan=100)
        self.LabelWindowFirstPopulation = Tk.Label(self.frame, text='', fg='red')
        self.LabelWindowFirstPopulation.pack(side=Tk.LEFT)
        #self.LabelWindowFirstPopulation.grid(row=0, column=1, rowspan=100)
        self.var = Tk.IntVar()
        self.generateRandom = Tk.Checkbutton(self.root, text="Generate static", variable=self.var, command=self.cb)
        #self.generateRandom.grid(row=10, column=7)
        self.randomPopulation = True

    def cb(self):

        self.randomPopulation = self.var.get()
        # print(self.randomPopulation)
    def createEnties(self):
        self.__crossoverProbabilityEntry = self.makeEntry(4, 7, 0.9, "Crossover probability")
        self.__mutationProbabilityEntry = self.makeEntry(5, 7, 0.1, "Mutation probability")
        self.__tournamenSelectionSize = self.makeEntry(8, 7, 6, "size of tournament")
        self.__tournamenSelectionSelect = self.makeEntry(9,7, 60, "amount of selections")
        self.__popSizeEntry = self.makeEntry(2, 7, 1000, "Population size")
        self.__routeSizeEntry = self.makeEntry(3, 7, 7, "Route size")
        self.__iterations = self.makeEntry(6, 7, 500, "Iterations")
        self.__instantions = self.makeEntry(7, 7, 1, "number of runs")

    def createFigures(self):
        self.leftFigure = Figure(figsize=(7, 7), dpi=60)
        self.leftSubplot = self.createSubplot(self.leftFigure, "Best of all")
        self.leftCanvas = self.createCanvas(self.leftFigure, self.frame0, 'LEFT')

        self.rightFigure = Figure(figsize=(7, 7), dpi=60)
        self.rightCanvas = self.createCanvas(self.rightFigure, self.frame0, 'RIGHT')
        self.rightSubplot = self.createSubplot(self.rightFigure, "Best of current generation")

        self.botLeftFigure = Figure(figsize=(7, 5), dpi=60)
        self.downLeftSubplot = self.createSubplot(self.botLeftFigure, "Best of current generation")
        self.downLeftCanvas = self.createCanvas(self.botLeftFigure, self.frame01, 'TOP')

        self.botRightFigure = Figure(figsize=(7, 5), dpi=60)
        self.downRightSubplot = self.createSubplot(self.botRightFigure, "Best of current generation")
        self.downRightCanvas = self.createCanvas(self.botRightFigure, self.frame01, 'BOTTOM')

    def createCanvas(self, figure, master, side):
        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()

        if side == 'LEFT':
            _side = Tk.LEFT
            #canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, rowspan=10)
            #canvas._tkcanvas.grid(row=0, column=0, columnspan=3, rowspan=10)
            canvas.get_tk_widget().pack(side=Tk.LEFT,anchor='nw')
           # canvas._tkcanvas.pack(side=Tk.LEFT,anchor='nw')
        elif side == 'RIGHT':
            _side = Tk.RIGHT
            #canvas.get_tk_widget().grid(row=0, column=3, columnspan=3, rowspan=10)
            #canvas._tkcanvas.grid(row=0, column=3, columnspan=3, rowspan=10)
            canvas.get_tk_widget().pack(side=Tk.LEFT,anchor='ne')
            canvas._tkcanvas.pack(side=Tk.LEFT,anchor='ne')
        elif side == 'TOP':
            _side = Tk.TOP
           # canvas.get_tk_widget().grid(row=10, column=0, columnspan=3, rowspan=10)
           # canvas._tkcanvas.grid(row=10, column=0, columnspan=3, rowspan=10)
            canvas.get_tk_widget().pack(side=Tk.RIGHT)
            canvas._tkcanvas.pack(side=Tk.RIGHT)
        elif side == 'BOTTOM':
            _side = Tk.BOTTOM
           # canvas.get_tk_widget().grid(row=10, column=3, columnspan=3, rowspan=10)
           # canvas._tkcanvas.grid(row=10, column=3, columnspan=3, rowspan=10),


            canvas.get_tk_widget().pack(side=Tk.RIGHT)
            canvas._tkcanvas.pack(side=Tk.RIGHT)
            #_side = Tk.e

        return canvas

    def makeEntry(self, row, column, value, text):

        # label = 'xdddd'
        #label.grid(row=row, column=column - 1)
        # e=Tk.simpledialog.askstring("File: ","Enter your file name")
        row = Tk.Frame(self.framebuttons)
        row.pack(side=Tk.TOP, fill=Tk.X)
        label = Tk.Label(row, text=text)
        entry = Tk.Entry(row)
        entry.pack(side=Tk.LEFT)
        label.pack(side=Tk.LEFT)
        entry.insert(0, value)
        return entry

    def createSubplot(self, figure, title, axes=[0, 800, 0, 800]):
        subplot = figure.add_subplot(111)
        # subplot.plot([0, 800, 0, 800], [0, 800, 0, 800], 'ro')
        subplot.set_title(title)
        subplot.set_xlabel('X')
        subplot.set_ylabel('Y')
        subplot.grid(True)
        subplot.set_xticks(np.arange(axes[0], axes[1], 100))
        subplot.set_yticks(np.arange(axes[2], axes[3], 100))
        return subplot

    def createButtons(self, master):
        row = Tk.Frame(master)
        row.pack(side=Tk.TOP, fill=Tk.X)
        button = Tk.Button(master=row, text='Start', command=self.start)
        button.pack(side=Tk.TOP)
       # button.grid(row=1, column=6)
        button2 = Tk.Button(master=row, text='Quit', command=self.quit)
        button2.pack(side=Tk.TOP)
        # button2.pack(side=Tk.BOTTOM)
        #button2.grid(row=1, column=7)
        button3 = Tk.Button(master=row, text='test', command=self.quit)
        button3.pack(side=Tk.TOP)
        # button3.pack(side=Tk.RIGHT)
        #button3.grid(row=1, column=8)

    def run(self):
        Tk.mainloop()

    def start(self):
        crossover_probability = float(self.__crossoverProbabilityEntry.get())
        mutation_probability = float(self.__mutationProbabilityEntry.get())
        population_size = int(self.__popSizeEntry.get())
        route_size = int(self.__routeSizeEntry.get())
        tournament_size = int(self.__tournamenSelectionSize.get())
        tournament_select = int(self.__tournamenSelectionSelect.get())
        self._GA = GA(chromosome_list, population_size, route_size, crossover_probability, mutation_probability,
                      test="TEST",
                      randomPopulation=self.randomPopulation,
                      graph=[self.leftSubplot, self.rightSubplot, self.downRightSubplot, self.downLeftSubplot],
                      canvas=[self.leftCanvas, self.rightCanvas, self.downRightCanvas, self.downLeftCanvas, ],
                      windows=[self.LabelWindowPopulation, self.LabelWindowFirstPopulation],
                      tournament_size = tournament_size, tournament_select = tournament_select
                      )

        print(self._GA)
        # self._GA = GA(chromosome_list, population_size, route_size, crossover_probability, mutation_probability, graph=[self.leftSubplot,self.rightSubplot,self.downRightSubplot, self.downLeftSubplot],canvas=[self.leftCanvas,self.rightCanvas, self.downRightCanvas, self.downLeftCanvas])
        threads = 0
        for i in range(0, int(self.__instantions.get()) - 1):
            x = GA(chromosome_list, population_size, route_size, crossover_probability, mutation_probability,
                   randomPopulation=self.randomPopulation,
                   graph=[self.leftSubplot, self.rightSubplot, self.downRightSubplot, self.downLeftSubplot],
                   canvas=[self.leftCanvas, self.rightCanvas, self.downRightCanvas, self.downLeftCanvas],
                   windows=[self.LabelWindowPopulation, self.LabelWindowFirstPopulation],
                   tournament_size = tournament_size, tournament_select = tournament_select
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
        pass
