# coding=utf-8
import Tkinter
from Tkinter import *
from tkFileDialog import *
import Tkinter as TK
import os.path


class Interface(Frame):
    """
    This class will manage the graphic part on the software.
    """

    def __init__(self):
        # Main window
        from projet import Chromosome, GeneticAlgorithm, Individual
        window = Tk()
        Frame.__init__(self, window, width=800, height=600, borderwidth=1)
        window.title('Genetic algorithm - Tool for comparison of genes expression and epigenetic data')

        self.C = Chromosome()
        self.G = GeneticAlgorithm(self.C)
        self.I = Individual()
        cadre = Frame()
        cadre.grid(sticky=W)
        self.file_path_coord = TK.StringVar()
        self.file_path_expr = TK.StringVar()
        self.mutation_rate = TK.StringVar()
        self.nb_individual = TK.StringVar()
        self.nb_run = TK.StringVar()
        self.time = TK.StringVar()
        self.nb_clust = TK.StringVar()


        # Part 1 - Load & Save file
        partOne = Tkinter.LabelFrame(window, text=" 1. Enter File : ")
        partOne.grid(row=0, columnspan=7, sticky='W', padx=5, pady=5, ipadx=15, ipady=5)
        # Select file coordinates
        selectFile = Tkinter.Label(partOne, text="Select your coordinates data file (.txt) :                ")
        selectFile.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        self.filePath = Tkinter.Entry(partOne, textvariable=self.file_path_coord)
        self.filePath.grid(row=0, column=1, columnspan=7, sticky="WE", pady=3)
        browseBtn = Tkinter.Button(partOne, text="Browse ...", command=self.browse_coord, underline=0)
        browseBtn.grid(row=0, column=8, sticky='W', padx=8, pady=2)
        # Select file expression
        selectFile2 = Tkinter.Label(partOne, text="Select your expression data file (.txt) :                ")
        selectFile2.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        self.filePath2 = Tkinter.Entry(partOne, textvariable=self.file_path_expr)
        self.filePath2.grid(row=1, column=1, columnspan=7, sticky="WE", pady=3)
        browseBtn2 = Tkinter.Button(partOne, text="Browse ...", command=self.browse_expr, underline=0)
        browseBtn2.grid(row=1, column=8, sticky='W', padx=8, pady=2)
        # Data visualization
        #preVisualization = Tkinter.Button(partOne, text="Pre visualize your data", command=self.preVisualizeE, underline=0)
        #preVisualization.grid(row=2, column=0, sticky='W', padx=5, pady=2)


        # Part 2 - Algorithm parameters
        partTwo = Tkinter.LabelFrame(window, text=" 2. Algorithm parameters ")
        partTwo.grid(row=2, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
        # Initial mutation rate
        mutationRate = Tkinter.Label(partTwo, text="Enter your mutation rate (0 to 100):")
        mutationRate.grid(row=3, column=0, sticky='W', padx=5, pady=2)
        mutationRateTxt = Tkinter.Entry(partTwo, textvariable=self.mutation_rate)
        mutationRateTxt.grid(row=3, column=1, columnspan=3, pady=2, sticky='WE')
        mutationRateCom = Tkinter.Label(partTwo, text="Generally initialize to 5% in order to obtain an equilibrate rate of mutation.\n", font=("arial", 8, "italic"))
        mutationRateCom.grid(row=4, column=0, sticky='W', padx=5, pady=2)
        # Number of individuals to generate
        indvNumber = Tkinter.Label(partTwo, text="Enter the number of individuals to generate (0 to 200):")
        indvNumber.grid(row=6, column=0, sticky='W', padx=5, pady=2)
        indvNumberTxt = Tkinter.Entry(partTwo, textvariable=self.nb_individual)
        indvNumberTxt.grid(row=6, column=1, columnspan=3, pady=2, sticky='WE')
        indvNumberCom = Tkinter.Label(partTwo, text="Initialized to 20 by default.\n", font=("arial", 8, "italic"))
        indvNumberCom.grid(row=7, column=0, sticky='W', padx=5, pady=2)
        # Number of clusters
        clustNumber = Tkinter.Label(partTwo, text="Indicate the percentage of cluster wanted (0 to 100)")
        clustNumber.grid(row=9, column=0, sticky='W', padx=5, pady=2)
        clustNumberTxt = Tkinter.Entry(partTwo, textvariable=self.nb_clust)
        clustNumberTxt.grid(row=9, column=1, columnspan=3, pady=2, sticky='WE')
        clustNumberCom = Tkinter.Label(partTwo, text="Initialized to 5% by default.\n", font=("arial", 8, "italic"))
        clustNumberCom.grid(row=10, column=0, sticky='W', padx=5, pady=2)
        # Number of run of the algorithm
        runAlgo = Tkinter.Label(partTwo, text="Select the number of run for the algorithm (50 to 100 000) :")
        runAlgo.grid(row=11, column=0, sticky='W', padx=5, pady=2)
        runAlgoSpb = TK.Spinbox(partTwo, from_=50, to=100000, increment=10, width=6, textvariable=self.nb_run)
        runAlgoSpb.grid(row=11, column=1, columnspan=3, sticky='E', padx=2, pady=3)
        # Fitness weight



        # Part 3 - Results
        partThree = Tkinter.LabelFrame(window, text=" 3. Results ")
        partThree.grid(row=5, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
        # Timer
        timer = Tkinter.Label(partThree, text="Timer (in seconds) :    ")
        timer.grid(row=3, column=0, sticky='W', padx=5, pady=2)
        timerTxt = Tkinter.Entry(partThree, textvariable=self.time)
        timerTxt.grid(row=4, column=0, columnspan=3, pady=2, sticky='W')
        # Visualize the result graph
        visualization = Tkinter.Button(partThree, text="Clustered graph 3D", command=self.visualize, underline=0)
        visualization.grid(row=7, column=0, sticky='W', padx=5, pady=2)


        # Menu
        menubar = Menu(window)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Load coordinates", command=self.browse_coord)
        menu1.add_command(label="Load expression", command=self.browse_expr)
        menu1.add_command(label="Save as", command=self.saveAs)
        menu1.add_separator()
        menu1.add_command(label="Quit", command=window.quit)
        menubar.add_cascade(label="File", menu=menu1)
        menu3 = Menu(menubar, tearoff=0)
        menu3.add_command(label="Manual", command=self.manual)
        menubar.add_cascade(label="Help", menu=menu3)
        window.config(menu=menubar)

        # Other buttons
        # Part Run
        runButton = Tkinter.Button(window, text="RUN", command=self.run, underline=0)
        runButton.grid(row=5, column=3, sticky='SE', padx=7, pady=7, ipadx=5, ipady=5)
        # Save file
        saveFile = Tkinter.Button(window, text="Save as", command=self.saveAs, underline=0)
        saveFile.grid(row=5, columnspan=6, sticky='SE', padx=5, pady=5, ipadx=5, ipady=5)
        # Quit
        quit = Button(window, text="Quit", command=window.destroy)
        quit.grid(row=5, columnspan=7, sticky='SE', padx=5, pady=5, ipadx=5, ipady=5)


        self.mutation_rate.trace_variable("w", self.mutationRate)
        self.nb_individual.trace_variable("w", self.indNumber)
        self.nb_clust.trace_variable('w', self.nbClust)
        self.nb_run.trace_variable("w", self.nbrun)

        self.grid_columnconfigure(0, weight=1)

        window.mainloop()



    # Functions
    def browse_coord(self):
        self.file_path_coord.set(askopenfilename())

    def browse_expr(self):
        self.file_path_expr.set(askopenfilename())


    def indNumber(self, name, index, mode):
        try:
            value = int(self.nb_individual.get())
            if 5 <= value <= 200:
                self.G.individualNumber = value
            else:
                self.nb_individual.set("")
        except:
            self.nb_individual.set("")


    def mutationRate(self, name, index, mode):
        try:
            value = float(self.mutation_rate.get())
            if 0 <= value <= 100:
                self.G.initialMutationRate = value
            else:
                self.mutation_rate.set("")
        except:
            self.mutation_rate.set("")


    def nbClust(self, name, index, mode):
        try:
            value = float(self.nb_clust.get())
            if 0 <= value <= 100:
                self.G.nb_clust = value
            else:
                self.nb_clust.set("")
        except:
            self.nb_clust.set("")


    def nbrun(self, name, index, mode):
        self.G.nb_run = int(self.nb_run.get())


    def timer(self):
        self.time.set(self.G.timer)


    def saveAs(self):
        self.G.save(asksaveasfilename())


    def about(self):
        winabout = Tk()
        winabout.title('About')
        ab = Tkinter.Label(winabout, text="This tool is a genetic algorithm who show the relationship between genes expression and epigenetic data of euclidian distance.\nFor more informaions reffers to the manual.")
        ab.grid(row=0, column=0, sticky='W', padx=10, pady=50)
        winabout.mainloop()


    def manual(self):
        winmanual = Tk()
        winmanual.title('Manual')
        man = Tkinter.Label(winmanual, text=open("users.txt", "r").read(), justify="left", wraplength=800)
        man.grid(row=0, column=0, sticky='W', padx=10, pady=50)
        winmanual.mainloop()
        pass

    def visualize(self):
        # dirname = askdirectory()
        # data2 = open(direname, 'r')
        # result = self.clusters(data2)
        pass


    def run(self):
        print 'log launch genetic algorithm with ' + str(self.G.individualNumber) + ' individual with a mutation rate of ' + str(self.G.initialMutationRate)
        self.C.fromfiles(self.file_path_coord.get(), self.file_path_expr.get())
        self.G.chromosome = self.C
        self.G.run()
        self.timer()


# Main
if __name__ == "__main__":
    Interface()