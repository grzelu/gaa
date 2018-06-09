import sys, time
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

class populationListWindow():
    def __init__(self):

        self.root = Tk.Tk()
        self.root.geometry("300x700")
        self.root.wm_title("Population list")
        self.frame = Tk.Frame(self.root)
        self.frame.pack()
        self.Label1 = Tk.Label(self.root,text='sdfdsf')
        self.Label1.pack()
        self.quitButton = Tk.Button(self.frame, text='Quit', width=25, command=self.close_window)
        self.quitButton.pack()
        #self.showPopulation([4, 1, 5, 67, 8])

    def windowRUN(self):
        print ("STARTUJEMY")
        self.root.mainloop()
    def close_window(self):
        self.root.destroy()
    def showPopulation(self,population):
        output = ''
        for i in population:
            output = output+str(i) + '\n'
        self.Label1['text'] = output




#xd = populationListWindow()
