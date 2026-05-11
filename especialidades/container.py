from tkinter import *
from tkinter import ttk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modulos.informacion import Informacion
from modulos.pedidos import Pedidos
from modulos.proveedor import Proveedor
from modulos.clientes import Clientes
from modulos.ventas import Ventas
from modulos.inventario import Inventario



class Container(ttk.Frame):
    def __init__(self, padre, controller):
        super().__init__(padre)
        self.controller = controller
        self.pack()
        self.place(x=0, y=0, width=1200, height=700)
        self.widgets()
        self.frames={}
        self.buttons=[]
        # va aqui
        for i in(Ventas,Inventario,Clientes,Pedidos,Proveedor,Informacion):
            frame=i(self)
            self.frames[i]=frame
            frame.pack()
            frame.config(bg="#C6D9E3",hightlightbackground="gray",highlightthickness=1)
            frame.place(x=0,y=40,width=1100,height=660)
        self.show_frame(Ventas)
    def show_frame(self, container):
        frame=self.frames[container]
        frame.tkraise()

    def widgets(self):
        pass