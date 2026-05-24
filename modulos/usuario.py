from tkinter import *
import tkinter as tk

class Usuario(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def widgets(self):
        pass