import matplotlib, time,random, threading, sys
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
        self.frame = Tk.Frame(self.root, bg='cyan', width=450, height=600, pady=3)
        self.frame.grid(column=10,row=0, sticky="ew",rowspan=10)
        self.leftFigure = Figure(figsize=(7, 7), dpi=60)
        self.leftSubplot = self.createSubplot(self.leftFigure, "Best of all")
        self.leftCanvas = self.createCanvas(self.leftFigure, self.root, 'LEFT')
        self.root.grid_rowconfigure(1, weight=1)
        self.rightFigure = Figure(figsize=(7, 7), dpi=60)
        self.rightCanvas = self.createCanvas(self.rightFigure,self.root,'RIGHT')
        self.rightSubplot = self.createSubplot(self.rightFigure, "Best of current generation")

        self.botLeftFigure = Figure(figsize=(7, 5), dpi=60)
        self.downLeftSubplot = self.createSubplot(self.botLeftFigure, "Best of current generation",axes=[0,100,0,100])
        self.downLeftCanvas = self.createCanvas(self.botLeftFigure, self.root, 'TOP')

        self.botRightFigure = Figure(figsize=(7, 5), dpi=60)
        self.downRightSubplot = self.createSubplot(self.botRightFigure, "Best of current generation",axes=[0,100,0,100])
        self.downRightCanvas = self.createCanvas(self.botRightFigure, self.root, 'BOTTOM')

        self.createButtons(self.root)
        self.__popSizeEntry = self.makeEntry(2,7,10,"Population size")
#        #chromosome_list, population_size, route_size, crossover_probability, mutation_probability
        self.__routeSizeEntry = self.makeEntry(3,7,11,"Route size")
        self.__crossoverProbabilityEntry = self.makeEntry(4,7,0.8,"Crossover probability")
        self.__mutationProbabilityEntry = self.makeEntry(5,7,0.08,"Mutation probability")
        self.__iterations = self.makeEntry(6, 7, 5, "Iterations")
        self.__instantions = self.makeEntry(7, 7, 1, "number of runs")
        #self.window = Tk.Toplevel(self.root)
        self.LabelWindowPopulation = Tk.Label(self.frame, text='your text',fg='blue')
        self.LabelWindowPopulation.grid(row=0,column=0,rowspan=100)
        self.LabelWindowFirstPopulation = Tk.Label(self.frame, text='first population',fg='red')
        self.LabelWindowFirstPopulation.grid(row=0,column=1,rowspan=100)
        self.var = Tk.IntVar()
        self.generateRandom = Tk.Checkbutton(self.root, text="Generate random", variable= self.var,command=self.cb)
        self.generateRandom.grid(row=8, column=7)
        self.randomPopulation=False
    def cb(self):

        self.randomPopulation = self.var.get()
        #print(self.randomPopulation)
    def createCanvas(self,figure,master,side):
        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()


        if side=='LEFT':
            _side = Tk.LEFT
            canvas.get_tk_widget().grid(row=0,column=0,columnspan=3, rowspan=10)
            canvas._tkcanvas.grid(row=0,column=0,columnspan=3, rowspan=10)
        elif side=='RIGHT':
            _side = Tk.RIGHT
            canvas.get_tk_widget().grid(row=0, column=3,columnspan=3, rowspan=10)
            canvas._tkcanvas.grid(row=0, column=3,columnspan=3, rowspan=10)
        elif side=='TOP':
            _side = Tk.TOP
            canvas.get_tk_widget().grid(row=10, column=0,columnspan=3, rowspan=10)
            canvas._tkcanvas.grid(row=10, column=0,columnspan=3, rowspan=10)
        elif side=='BOTTOM':
            _side = Tk.BOTTOM
            canvas.get_tk_widget().grid(row=10, column=3,columnspan=3, rowspan=10)
            canvas._tkcanvas.grid(row=10, column=3,columnspan=3, rowspan=10)
            _side = Tk.TOP

        return canvas
    def makeEntry(self, row,column,value,text):
        label = Tk.Label(self.root,text = text)
       # label = 'xdddd'
        label.grid(row=row,column=column-1)
       # e=Tk.simpledialog.askstring("File: ","Enter your file name")
        entry = Tk.Entry(self.root, width=20)
        entry.grid(row=row, column = column)
        entry.insert(0,value)
        return entry
    def createSubplot(self, figure, title, axes = [0, 800, 0, 800]):
        subplot = figure.add_subplot(111)
        #subplot.plot([0, 800, 0, 800], [0, 800, 0, 800], 'ro')
        subplot.set_title(title)
        subplot.set_xlabel('X')
        subplot.set_ylabel('Y')
        subplot.grid(True)
        subplot.set_xticks(np.arange(axes[0], axes[1], 20))
        subplot.set_yticks(np.arange(axes[2], axes[3], 20))
        return subplot
    def createButtons(self,master):
        button = Tk.Button(master=master, text='Start', command=self.start)
        button.grid(row=1,column=6)
        button2 = Tk.Button(master=master, text='Quit', command=self.quit)
        #button2.pack(side=Tk.BOTTOM)
        button2.grid(row=1,column=7)
        button3 = Tk.Button(master=master, text='test', command=self.quit)
       # button3.pack(side=Tk.RIGHT)
        button3.grid(row=1,column=8)

    def run(self):
        Tk.mainloop()

    def start(self):
        crossover_probability = float(self.__crossoverProbabilityEntry.get())
        mutation_probability = float(self.__mutationProbabilityEntry.get())
        population_size = int(self.__popSizeEntry.get())
        route_size = int(self.__routeSizeEntry.get())

        self._GA = GA(chromosome_list, population_size, route_size, crossover_probability, mutation_probability,
                      test="TEST",
                      randomPopulation=self.randomPopulation,
                      graph=[self.leftSubplot,self.rightSubplot,self.downRightSubplot, self.downLeftSubplot],
                      canvas=[self.leftCanvas,self.rightCanvas, self.downRightCanvas, self.downLeftCanvas,],
                      windows =  [self.LabelWindowPopulation,self.LabelWindowFirstPopulation]
                      )

        #self._GA = GA(chromosome_list, population_size, route_size, crossover_probability, mutation_probability, graph=[self.leftSubplot,self.rightSubplot,self.downRightSubplot, self.downLeftSubplot],canvas=[self.leftCanvas,self.rightCanvas, self.downRightCanvas, self.downLeftCanvas])
        print (self._GA)
        threads = 0
        for i in range(0,int(self.__instantions.get())-1):
            x = GA(chromosome_list, population_size, route_size, crossover_probability, mutation_probability,
                   randomPopulation=self.randomPopulation,
                   graph=[self.leftSubplot, self.rightSubplot, self.downRightSubplot, self.downLeftSubplot],
                   canvas=[self.leftCanvas, self.rightCanvas, self.downRightCanvas, self.downLeftCanvas],
                   windows =  [self.LabelWindowPopulation,self.LabelWindowFirstPopulation]
                   )

            self.i = threading.Thread(target=self.updateGraph, args=(x,))
            threads+=1
            self.i.start()
        self.new_thread = threading.Thread(target=self.updateGraph, args=(self._GA,))
        self.new_thread.start()
        print ("Number of threads: {}".format(threads))
    def updateGraph(self,thr):
        thr.startGA(n_iterations = int(self.__iterations.get()))

    def quit(self):
        pass
