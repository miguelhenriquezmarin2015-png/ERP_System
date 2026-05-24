from tkinter import *
from tkinter import ttk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modulos.login import Login
from modulos.login import Registro
from especialidades.container import Container

class Manager(Tk):
    def __init__(self, *args,**kwagrs):
        super().__init__(*args,**kwagrs)
        self.title("Mini Marker")
        self.geometry("1200x700+120+20")
        self.resizable(False,False)

        container=Frame(self)
        container.pack(side=TOP,fill=BOTH,expand=True)
        container.configure(bg="#C6D9E3")

        self.frames={}
        for i in(Login,Registro,Container):
            frame=i(container, self)
            self.frames[i]=frame
            frame.grid(row=0,column=0,sticky="nsew")
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)
        #cambiar aqui al terminar el programa
        self.show_frame(Container)

        self.style=ttk.Style()
        self.style.theme_use("clam")
    
    def show_frame(self,container):
        frame=self.frames[container]
        frame.tkraise()

def main():
    app=Manager()
    app.mainloop()

if __name__=="main":
    main()