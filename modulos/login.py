from tkinter import *
import tkinter as tk

class Login(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def widgets(self):
        pass

class Registro(tk.Frame):
    def __init__(self, padre,controler):
        super().__init__(padre)
        self.controler=controler
        self.widgets()

    def widgets(self):
        pass