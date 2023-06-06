# by Clexxcraft + Taba
import tkinter, os, math
from tkinter import ttk
from tkinter import filedialog as fd
import re


"""
///
todo:
machen dass man die einzelnen spektren wieder schließen kann
interpolation pro ding machen
jeder graph farbe wählbar
verschiedene graphen verrechnen




"""

def subtract_graphs(g1x, g1y, g2x, g2y):
    g3x = []
    g3y = []
    g4x = []
    g4y = []
    c1 = 0
    c2 = 0
    for c in range(max(g1x[0], g2x[0]), min(g1x[1], g2x[1])):
        while c > g1x[c1]:
            c1 += 1
        while c > g2x[c2]:
            c2 += 1
        g3x.append(c)
        g3y.append(((g1y[c1]/(g1x[c1]-c))+(g1y[c1+1]/(g1x[c1+1]-c)))*(g1x[c1+1]+g1x[c1]-c-c))
        g4x.append(c)
        g4y.append(((g2y[c2]/(g2x[c2]-c))+(g2y[c2+1]/(g2x[c2+1]-c)))*(g2x[c2+1]+g2x[c2]-c-c))
    for i in range(len(g3x)):
        g3y[i] += g4y[i]
    return g3x, g3y


def floattable(s):
    if s.count(".") > 1:
        return False
    for i in s:
        if not i in ["1","2","3","4","5","6","7","8","9","0","."]:
            return False
    return True
def get_average(lst):
    lst = [l for l in lst if not type(l)==complex and not l == None]
    amount = len(lst)
    if amount > 0:
        average = sum(lst)/amount
        variance = math.sqrt(sum([(l-average)**2 for l in lst])/amount)
        new_lst = [l for l in lst if l <= average+variance*1.1 and l >= average-variance*1.1]
        return (sum(new_lst)/len(new_lst), variance)
    else:
        return None

class Read:
    def __init__(self, data):
        self.raw = data
    def get(self,typ):
        ret_x = []
        ret_y = []
        if typ == "txt":
            data = self.raw.replace("\r","").replace("\t"," ").split("\n")
            for d in data:
                d = [float(i.replace(",",".")) if not i == '' else None for i in d.split(" ")]
                while None in d:
                    del d[d.index(None)]
                if len(d) < 2:
                    continue
                ret_x.append(d[0])
                ret_y.append(d[1])
        elif typ == "jdx":
            data = self.raw.replace("\r","").replace("\t"," ").split("\n")
            for d in data:
                if len(d) < 1:
                    continue
                if d[0] == "#":
                    continue
                d = [float(i.replace(",",".")) if not i == '' and floattable(i.replace(",",".")) else None for i in d.split(" ")]
                while None in d:
                    del d[d.index(None)]
                if len(d) < 2:
                    continue
                ret_x.append(d[0])
                ret_y.append(d[1])
        else:
            raise Exception("Unknown Data Format")
        return ret_x, ret_y

class SpectroPlot:
    def add_tab(self, name="+"):
        
        self.frames.append(ttk.Frame(self.tabs))
        self.tabs.add(self.frames[-1], text = name)
        self.tabs.tab("current", text="Input "+str(self.index))
        self.files["Input "+str(self.index)] = None
        b1 = tkinter.Button(self.frames[-1], text="Open File")
        b1.bind("<Button-1>", lambda x: self.open_file(x))
        b1.grid(column=0, row=1, padx=5, pady=5)
        l2 = tkinter.Label(self.frames[-1], text="No File selected")
        l2.grid(column=1, row=1, padx=5, pady=5)

        # interpolation
        l1 = tkinter.Label(self.frames[-1], text="Interpolation")
        l1.grid(column=0, row=2)
        polation = ttk.Scale(self.frames[-1], from_=1, to=50, command=lambda x: self.change_polation(x), orient='horizontal')
        polation.grid(column=1, columnspan=3, row=2, sticky="ew")
        self.polation["Input "+str(self.index)] = 1
        self.pl1["Input "+str(self.index+1)] = tkinter.Label(self.frames[-1], text="1")
        self.pl1["Input "+str(self.index+1)].grid(column=4, row=2)

        # color selection
        co = ["red", "green", "blue", "purple", "orange"]
        var2 = tkinter.StringVar(self.frames[-1])
        self.cl1["Input "+str(self.index)] = ttk.OptionMenu(self.frames[-1], var2, co[0], *co, command=lambda x: self.change_color(x))
        self.cl1["Input " + str(self.index)].grid(column=0, row=3)
        self.color["Input " + str(self.index)] = co[0]

        # calc
        cl = tkinter.Label(self.frames[-1], text="Calculation:")
        cl.grid(column=0, row=4)
        self.ci["Input "+str(self.index)] = ttk.Entry(self.frames[-1])  # Entry.get() um den Inhalt zu erfahren
        self.ci["Input " + str(self.index)].grid(column=1, row=4)
        self.calc["Input " + str(self.index)] = ""

        self.index += 1
    def open_file(self, event):
        filename = fd.askopenfilename()
        name = event.widget.master.master.tab('current')['text']
        label = None
        for i in event.widget.master.winfo_children():
            if isinstance(i, tkinter.Label):
                if i.grid_info()['row'] == 1:
                    label = i
        if filename:
            label.configure(text="File: "+filename)
            self.files[name] = filename
        else:
            label.configure(text="No File selected")
            self.files[name] = None
    def change_polation(self,event):
        self.pl1[self.tabs.tab('current')['text']].configure(text=str(round(float(event))))
        self.polation[self.tabs.tab('current')['text']] = round(float(event))
    def change_color(self,event):
        self.cl1[self.tabs.tab('current')['text']].configure(text=str(event))
        self.color[self.tabs.tab('current')['text']] = event
    def __init__(self):
        self.ci = {}
        self.calc = {}
        self.pl1 = {}
        self.polation = {}
        self.cl1 = {}
        self.color = {}
        self.files = {}
        self.mode = {}
        self.index = 0
        self.window = tkinter.Tk()
        self.window.title("SpectroPlot")
        self.window.geometry("800x600")
        self.window.columnconfigure(0,weight=1, uniform="foo")
        self.window.rowconfigure(3,weight=1,uniform="foo")
        # Inputs
        inputs = ttk.LabelFrame(self.window, text="Inputs")
        self.tabs = ttk.Notebook(inputs)
        self.frames = []
        self.add_tab()
        self.add_tab()
        self.tabs.pack(fill="both")
        inputs.grid(column=0,row=0,sticky="ew", padx=5, pady=5)
        self.tabs.bind('<<NotebookTabChanged>>', lambda x: self.change(x))
        # Options
        options = ttk.LabelFrame(self.window, text="Options")
        for i in range(6):
            options.columnconfigure(i,weight=int(800/6),uniform="foo")
        options.columnconfigure(4,weight=10,uniform="foo")
        options.grid(column=0,row=1,padx=5,pady=5, sticky="ew")
        # Rest
        bp = tkinter.Button(self.window, text="Plot")
        bp.grid(column=0,row=2,sticky="ew", padx=5, pady=5)
        bp.bind("<Button-1>", lambda x: self.plot(x))
        plot = ttk.LabelFrame(self.window, text="Plot")
        self.canvas = tkinter.Canvas(plot, bg="white")
        self.canvas.pack(fill="both", expand=True)
        plot.grid(column=0,row=3, sticky='ewsn', padx=5, pady=5)
    def plot(self, event):
        self.data = []
        start_x = 0
        end_x = 0
        start_y = 0
        end_y = 0
        x_scala_start = float('inf')
        x_scala_end = 0
        y_scala_start = float('inf')
        y_scala_end = 0
        print("Start Ploting")
        self.canvas.delete('all')
        for key in list(self.files.keys()):
            if self.files[key] == None:
                continue
            with open(self.files[key],"r") as file:
                data = file.read()
            r = Read(data)
            _, extension = os.path.splitext(self.files[key])
            x, y = r.get(extension[1:])
            start_x = min(x)
            end_x = max(x)
            start_y = min(y)
            end_y = max(y)
            x_scala_start = start_x if start_x < x_scala_start else x_scala_start
            x_scala_end = end_x if end_x > x_scala_end else x_scala_end
            y_scala_start = start_y if start_y < y_scala_start else y_scala_start
            y_scala_end = end_y if end_y > y_scala_end else y_scala_end
            data_y = []
            ydata = []
            for i in range(len(x)):
                pos_x = self.canvas.winfo_width()-int((x[i]-x_scala_start)/(x_scala_end-x_scala_start)*self.canvas.winfo_width())
                pos_y = int((y[i]-start_y)/(end_y-start_y)*self.canvas.winfo_height())
                data_y.append(pos_y)
                if len(data_y) > self.polation[key]:
                    data_y.pop(0)
                average_y = int(sum(data_y)/len(data_y))
                ydata.append(average_y)
            self.data.append([x,ydata])
        for i in range(10,self.canvas.winfo_width(),10):
            if i%50 == 0:
                self.canvas.create_line(i,0,i,self.canvas.winfo_height(), fill="grey", width=2)
                self.canvas.create_text(i,self.canvas.winfo_height()-20, text=str(int(round(x_scala_end-((x_scala_end-x_scala_start)*i/self.canvas.winfo_width()),0))), font=("Arial 13"))
            else:
                self.canvas.create_line(i,0,i,self.canvas.winfo_height(), fill="grey")
        c = 0
        for d in self.data:
            # list(self.files.keys())[c+1] = key
            d = self.calculate(list(self.files.keys())[c+1], d)
            x, y = d
            avg, varience = get_average(y)
            start_x = min(x)
            end_x = max(x)
            start_y = min(y)
            end_y = max(y)
            prev_x = self.canvas.winfo_width()-int((x[0]-x_scala_start)/(x_scala_end-x_scala_start)*self.canvas.winfo_width())
            prev_y = self.canvas.winfo_height()-int((y[0]-start_y)/(end_y-start_y)*self.canvas.winfo_height())
            data_y = [prev_y]
            prev_average_y = prev_y
            for i in range(1,len(x)):
                pos_x = self.canvas.winfo_width()-int((x[i]-x_scala_start)/(x_scala_end-x_scala_start)*self.canvas.winfo_width())
                pos_y = self.canvas.winfo_height()-int((y[i]-start_y)/(end_y-start_y)*self.canvas.winfo_height())
                data_y.append(pos_y)
                if len(data_y) > self.polation[key]:
                    data_y.pop(0)
                average_y = int(sum(data_y)/len(data_y))
                self.canvas.create_line(prev_x,prev_average_y,pos_x,average_y,fill=self.color[list(self.files.keys())[c+1]], width=2)
                prev_average_y = average_y
                prev_x = pos_x
                prev_y = pos_y
            c+=1
        print("End Ploting")
    def calculate(self, key, data):
        if self.ci[key].get() != "":
            a = re.split('[-+]',self.calc[key])
            print(a)
        return data
    def change(self, event):
        name = event.widget.tab('current')['text']
        if name=="+":
            self.add_tab()
    def mainloop(self):
        self.window.mainloop()

if __name__ == "__main__":
    sp = SpectroPlot()
    sp.mainloop()
