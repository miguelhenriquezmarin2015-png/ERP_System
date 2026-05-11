from tkinter import *
from tkinter import Tk
from tkinter import ttk

class Login(ttk.Frame):
    def __init__(self, padre, controller):
        super().__init__(padre)
        self.controller = controller
        self.widgets()

    def widgets(self):
        pass

class Registro(ttk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def widgets(self):
        pass