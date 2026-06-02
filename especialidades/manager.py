from tkinter import *
from tkinter import ttk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modulos.login import Login
from especialidades.container import Container
from modulos.inventario import Inventario


class Manager(Tk):
    def __init__(self, *args,**kwagrs):
        super().__init__(*args,**kwagrs)
        self.title("Mini Market")
        self.geometry("1200x700+120+20")
        self.resizable(False,False)
        self.alertas_mostradas = False 

        container=Frame(self)
        container.pack(side=TOP,fill=BOTH,expand=True)
        container.configure(bg="#C6D9E3")

        self.frames={}
        for i in(Login,Container):
            frame=i(container, self)
            self.frames[i]=frame
            frame.grid(row=0,column=0,sticky="nsew")
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)
        #cambiar aqui al terminar el programa
        self.show_frame(Login)

        self.style=ttk.Style()
        self.style.theme_use("clam")
    
    def show_frame(self,ventana_clases):
        frame=self.frames[ventana_clases]
        frame.tkraise()
        if ventana_clases.__name__ == "Container" or ventana_clases == Container:
            if Inventario in self.frames:
                self.frames[Inventario].verificar_alertas_stock()
                self.frames[Inventario].verificar_alertas_vencimiento()
                
        return frame
    
def main():
    app=Manager()
    app.mainloop()

if __name__=="__main__":
    main()