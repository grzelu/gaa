import matplotlib, time,random, threading, sys
from ga import GA
from variables import *
from queue import Queue
matplotlib.use('TkAgg')

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
        self.root.geometry("800x600")
        self.root.wm_title("Genetic Algorythm")

        self.fig1 = Figure(figsize=(7, 7), dpi=60)
        self.fig2 = Figure(figsize=(7, 7), dpi=60)
        self.upperSubplot = self.createSubplot(self.fig1,"Best of all")
        self.bottomSubplot = self.createSubplot(self.fig2, "Best of current generation")
        self.canvas1 = self.createCanvas(self.fig1,self.root,'LEFT')
        self.canvas2 = self.createCanvas(self.fig2,self.root,'RIGHT')
        self.createButtons(self.root)
        self.makeEntry(4,5)

    def createCanvas(self,figure,master,side):
        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()
        if side=='LEFT':
            _side = Tk.LEFT
            canvas.get_tk_widget().grid(row=0,column=0,columnspan=3)
            canvas._tkcanvas.grid(row=0,column=0,columnspan=3)
        elif side=='RIGHT':
            _side = Tk.RIGHT
            canvas.get_tk_widget().grid(row=0, column=3,columnspan=3)
            canvas._tkcanvas.grid(row=0, column=3,columnspan=3)
        elif side=='TOP':
            _side = Tk.TOP
            canvas.get_tk_widget().grid(row=1, column=0,columnspan=3)
            canvas._tkcanvas.grid(row=1, column=0,columnspan=3)
        elif side=='BOTTOM':
            _side = Tk.BOTTOM
            canvas.get_tk_widget().grid(row=1, column=3,columnspan=3)
            canvas._tkcanvas.grid(row=1, column=3,columnspan=3)
            _side = Tk.TOP
       # canvas = FigureCanvasTkAgg(figure, master=master)
       # canvas.draw()
        #canvas.get_tk_widget().pack(side=_side, fill=Tk.NONE)
       # canvas._tkcanvas.pack(side=_side, fill=Tk.NONE)
        #canvas.get_tk_widget().grid(row=0)
        #canvas._tkcanvas.grid(row=0)


        return canvas
    def makeEntry(self, row,column):
       # e=Tk.simpledialog.askstring("File: ","Enter your file name")
        entry = Tk.Entry(self.root, width=20)
        entry.grid(row=row, column = column)
        pass
    def createSubplot(self, figure, title):
        subplot = figure.add_subplot(111)
        subplot.plot([0, 800, 0, 800], [0, 800, 0, 800], 'ro')
        subplot.set_title(title)
        subplot.set_xlabel('X')
        subplot.set_ylabel('Y')
        subplot.grid(True)
        subplot.set_xticks(np.arange(0, 800, 20))
        subplot.set_yticks(np.arange(0, 800, 20))
        return subplot
    def createButtons(self,master):
        button = Tk.Button(master=master, text='Start', command=self.start)
        button.grid(row=2,column=0)
        button2 = Tk.Button(master=master, text='Quit', command=self.quit)
        #button2.pack(side=Tk.BOTTOM)
        button2.grid(row=2,column=1)
        button3 = Tk.Button(master=master, text='test', command=self.quit)
       # button3.pack(side=Tk.RIGHT)
        button3.grid(row=2,column=2)

    def run(self):
        Tk.mainloop()

    def start(self):
        print ("XD")
        self._GA = GA(chromosome_list, population_size, route_size, crossover_probability, mutation_probability, graph=self.upperSubplot,
                 canvas=self.canvas1)
        print (self._GA)
        self.new_thread = threading.Thread(target=self.updateGraph)
        self.new_thread.start()
        print (self.new_thread)
        #self.new_thread = threading.Thread(target=self.updateGraph, kwargs={"ga": self._GA, "canvas": self.canvas1})
    def updateGraph(self):
        #self.new_thread = threading.currentThread()
        print("updateGraph")
        new_thread = threading.currentThread()
        self._GA.startGA()
    def quit(self):
        pass
