import matplotlib, time,random, threading, sys
from queue import Queue
from ga import GA
from main import chromosome_list, population_size, route_size, crossover_probability, mutation_probability
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk


def destroy(e):
    sys.exit()

root = Tk.Tk()
root.wm_title("Embedding in TK")


f = Figure(figsize=(4, 3), dpi=100)
a = f.add_subplot(111)
a.plot([0,800,0,800], [0,800,0,800], 'ro')
a.set_title('Tk embedding')
a.set_xlabel('X axis label')
a.set_ylabel('Y label')
a.grid(True)

f2 = Figure(figsize=(4,3), dpi=100)
nowe = f2.add_subplot(111)
nowe.grid(True)
nowe.plot([0,800,0,800], [0,800,0,800], 'ro')
nowe.set_title('Bierzaca populacja')
nowe.set_xlabel("X")
nowe.set_ylabel("Y")
#nowe.plot(t,s)
# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.X, expand=0)


canvas2 = FigureCanvasTkAgg(f2,master=root)
canvas2.draw()
canvas2.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
canvas2._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

def updateGraph(ga=None,canvas=None):
    new_thread=threading.currentThread()
    ga.start()
   #while getattr(new_thread, "do_run", True):
   #     print ("XD")
   #
    #    #nowe.clear()
     #   nowe.plot(random.sample(range(0,100),20))
      #  canvas2.draw()
       # time.sleep(1)
    #print ("STOP")
gaa = GA(chromosome_list, population_size, route_size, crossover_probability, mutation_probability, graph=a, canvas=canvas)
new_thread = threading.Thread(target=updateGraph,kwargs = {"ga": gaa, "canvas":canvas})
def start():
    #thread_queue = queue
    global new_thread,gaa
    try:
        new_thread.start()
    except RuntimeError:
        new_thread = threading.Thread(target=updateGraph,kwargs = {"ga": gaa, "canvas":canvas})
        start()
def quit():
    new_thread.do_run=False
    print ("STOPPING THREAD")
    #time.sleep(10)
    #sys.quit()
button = Tk.Button(master=root, text='Start', command=start)
button.pack(side=Tk.BOTTOM)
button2 = Tk.Button(master=root, text='Quit', command=quit)
button2.pack(side=Tk.BOTTOM)
#print (random.sample(range(1000),10))
#Tk.mainloop()

Tk.mainloop()
