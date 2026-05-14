#import controler
from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox,filedialog

class Inventario(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def widgets(self):
        canvas_articulos=tk.Label(self,text="ARTICULOS",font="arial 20 bold",bg="#C6D9E3")
        canvas_articulos.place(x=300,y=10,width=900,height=590)

        self.canvas=tk.Canvas(canvas_articulos)
        self.scrollbar=Scrollbar(canvas_articulos,orient="vertical",command=self.canvas.yview)
        self.scrollbar_frame=tk.Frame(self.canvas,bg="#C6D9E3")
        self.scrollbar_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0,0),window=self.scrollbar_frame,anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left",fill="both",expand=True)
#buscador
        frame_buscar=LabelFrame(self,text="BUSCAR",font="arial 14 bold",bg="#C6D9E3")
        frame_buscar.place(x=10,y=10,width=280,height=80)

        self.combobox_buscar=ttk.Combobox(frame_buscar,font="arial 12",)
        self.combobox_buscar.place(x=10,y=5,width=250,height=40 )
#seleccionar
        frame_seleccionar=LabelFrame(self,text="SELECCIONAR",font="arial 14 bold",bg="#C6D9E3")
        frame_seleccionar.place(x=10,y=100,width=280,height=80)

"""class Inventario:
    def __init__(self,_id,_nombre,_cantidad,_precio):
        self.id=_id
        self.nombre=_nombre
        self.cantidad=_cantidad
        self.precio=_precio
    def get_id(self):
        return self.id
    def get_nombre(self):
        return self.nombre
    def get_cantidad(self):
        return self.cantidad
    def get_precio(self):
        return self.precio
    def get_precio(self,id):
        controler.mostar_id()
    def get_cantidadbaja(self):
        controler.mostrar_inventario_baja_cantidad()
        """