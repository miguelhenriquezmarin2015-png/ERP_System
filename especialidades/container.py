from tkinter import *
import tkinter as tk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modulos.informacion import Informacion
from modulos.pedidos import Pedidos
from modulos.proveedor import Proveedor
from modulos.clientes import Clientes
from modulos.ventas import Ventas
from modulos.inventario import Inventario

class Container(tk.Frame):
    def __init__(self, padre, controller):
        super().__init__(padre)
        self.controller = controller
        
        self.frames={}
        self.buttons=[]
        
        for i in(Ventas,Inventario,Clientes,Pedidos,Proveedor,Informacion):
            frame=i(self,controller)
            self.frames[i]=frame
            frame.config(bg="#C6D9E3",highlightbackground="gray",highlightthickness=1)
            frame.place(x=0,y=50,width=1200,height=650)
            
        self.widgets()
        #cambiar aqui al terminar
        self.show_frames(Ventas)
        
        controller.protocol("WM_DELETE_WINDOW", self.al_cerrar_programa)
        
    def show_frames(self, ventas_clase):
        frame=self.frames[ventas_clase]
        frame.tkraise()
        
    def al_cerrar_programa(self):
        instancia_ventas = self.frames.get(Ventas)
        if instancia_ventas:
            instancia_ventas.cancelar_toda_la_venta()
        self.controller.destroy()

    def ventas(self):
        self.show_frames(Ventas)
    def inventario(self):
        self.show_frames(Inventario)
    def clientes(self):
        self.show_frames(Clientes)
    def pedidos(self):
        self.show_frames(Pedidos)
    def proveedor(self):
        self.show_frames(Proveedor)
    def informacion(self):
        self.show_frames(Informacion)

    def widgets(self):
        frame2=tk.Frame(self,bg="gray")
        frame2.place(x=0,y=0,width=1200,height=50)

        self.btn_ventas=Button(frame2,fg="black",text="Ventas",font="sans 16 bold",command=self.ventas)
        self.btn_ventas.place(x=0,y=0,width=200,height=50)

        self.btn_inventario=Button(frame2,fg="black",text="Inventario",font="sans 16 bold",command=self.inventario)
        self.btn_inventario.place(x=200,y=0,width=200,height=50)

        self.btn_clientes=Button(frame2,fg="black",text="Clientes",font="sans 16 bold",command=self.clientes)
        self.btn_clientes.place(x=400,y=0,width=200,height=50)

        self.btn_pedidos=Button(frame2,fg="black",text="Pedidos",font="sans 16 bold",command=self.pedidos)
        self.btn_pedidos.place(x=600,y=0,width=200,height=50)

        self.btn_proveedor=Button(frame2,fg="black",text="Proveedor",font="sans 16 bold",command=self.proveedor)
        self.btn_proveedor.place(x=800,y=0,width=200,height=50)

        self.btn_informacion=Button(frame2,fg="black",text="Información",font="sans 16 bold",command=self.informacion)
        self.btn_informacion.place(x=1000,y=0,width=200,height=50)

        self.buttons=[self.btn_ventas,self.btn_inventario,self.btn_clientes,self.btn_pedidos,self.btn_proveedor,self.btn_informacion]
        frame2.tkraise()
