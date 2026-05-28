from tkinter import *
from tkinter import ttk,messagebox
import tkinter as tk
import modulos.controlador as ctrl

class Pedidos(tk.Frame):
    def __init__(self,padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def widgets(self):
        pass