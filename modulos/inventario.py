#import controler
from tkinter import *
import tkinter as tk

class Inventario(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def widgets(self):
        pass
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