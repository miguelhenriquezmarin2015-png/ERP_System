from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys

class Login(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.place(x=0,y=0,width=1200,height=700)
        self.controller=controller
        self.widgets()

    def widgets(self):
        fondo=tk.Frame(self,bg="#C6D9E3")
        fondo.place(x=0,y=0,width=1200,height=700)

        self.bg_imagen=Image.open("imagenes/login.jpg")
        self.bg_imagen=self.bg_imagen.resize((1200,700))
        self.bg_imagen=ImageTk.PhotoImage(self.bg_imagen)
        self.bg_label=ttk.Label(fondo,image=self.bg_imagen)
        self.bg_label.place(x=0,y=0,width=1200,height=700)

        frame1=tk.Frame(self,bg="#FFFFFF",highlightbackground="black",highlightthickness=1)
        frame1.place(x=350,y=70,width=400,height=560)

        user=ttk.Label(frame1,text="Nombre de Usuario",font="arial 16 bold",background="#FFFFFF")
        user.place(x=100,y=180)
        self.username=ttk.Entry(frame1,font="arial 14",background="#C6D9E3")
        self.username.place(x=100,y=220,width=200,height=30)

        pas=ttk.Label(frame1,text="Contraseña",font="arial 16 bold",background="#FFFFFF")
        pas.place(x=100,y=280)
        self.password=ttk.Entry(frame1,font="arial 14",background="#C6D9E3",show="*")
        self.password.place(x=100,y=320,width=200,height=30)

class Registro(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def widgets(self):
        pass