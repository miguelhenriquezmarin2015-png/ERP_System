import tkinter as tk
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
import sys 
import os
from modulos.ventas import Ventas
from modulos import controler

# --- CLASE BASE (LÓGICA COMPARTIDA) ---
class PantallaBase(tk.Frame):
    def __init__(self, padre, controller):
        super().__init__(padre)
        self.controller = controller

    def crear_fondo_comun(self):
        fondo = tk.Frame(self, bg="#C6D9E3")
        fondo.place(x=0, y=0, width=1200, height=700)
        try:
            # Usamos la misma imagen para mantener la estética
            self.bg_imagen = Image.open("imagenes/login.jpg")
            self.bg_imagen = self.bg_imagen.resize((1200, 700))
            self.bg_imagen = ImageTk.PhotoImage(self.bg_imagen)
            tk.Label(fondo, image=self.bg_imagen).place(x=0, y=0, width=1200, height=700)
        except:
            print("Imagen de fondo no encontrada")

    def configurar_animacion(self, entry, label, y_sube, y_baja):
        entry.bind("<FocusIn>", lambda e: self.subir(label, y_sube))
        entry.bind("<FocusOut>", lambda e: self.bajar(label, entry, y_baja))
        label.bind("<Button-1>", lambda e: entry.focus_set())
        label.lift()

    def subir(self, label, nueva_y):
        label.place(y=nueva_y)
        label.config(font=("arial", 10, "bold"), fg="#2196F3")

    def bajar(self, label, entry, y_original):
        if not entry.get():
            label.place(y=y_original)
            label.config(font=("arial", 12), fg="gray")
            label.lift()

    def limpiar_campos(self, *entries):
        for entry in entries:
            entry.delete(0, tk.END)

    def validacion(self, user,pas):
        return len(user) > 0 and len(pas) > 0

# --- CLASE LOGIN ---
class Login(PantallaBase):
    def __init__(self, padre, controller):
        super().__init__(padre, controller)
        self.widgets()

    def widgets(self):
        self.crear_fondo_comun()
        
        frame_login = tk.Frame(self, bg="#FFFFFF", highlightbackground="#D3D3D3", highlightthickness=1)
        frame_login.place(x=400, y=100, width=400, height=500)

        # Campos Usuario y Password
        self.lbl_u = tk.Label(frame_login, text="Nombre de Usuario", font="arial 12", bg="white", fg="gray")
        self.lbl_u.place(x=70, y=180)
        self.ent_u = tk.Entry(frame_login, font="arial 14", bd=0, highlightthickness=1, highlightbackground="lightgray")
        self.ent_u.place(x=70, y=180, width=260, height=35)
        self.configurar_animacion(self.ent_u, self.lbl_u, 155, 180)

        self.lbl_p = tk.Label(frame_login, text="Contraseña", font="arial 12", bg="white", fg="gray")
        self.lbl_p.place(x=70, y=260)
        self.ent_p = tk.Entry(frame_login, font="arial 14", bd=0, highlightthickness=1, highlightbackground="lightgray", show="*")
        self.ent_p.place(x=70, y=260, width=260, height=35)
        self.configurar_animacion(self.ent_p, self.lbl_p, 235, 260)

        # Botones
        tk.Button(frame_login, text="INICIAR SESIÓN",command=self.login, bg="#2196F3", fg="white", font="arial 12 bold", bd=0, cursor="hand2").place(x=70, y=340, width=260, height=45)
        
        # Este botón ahora nos lleva a la clase Registro
        """tk.Button(frame_login, text="REGISTRARSE", bg="#4CAF50", fg="white", font="arial 12 bold", bd=0, cursor="hand2",
                  command=lambda: self.controller.show_frame(Registro)).place(x=70, y=400, width=260, height=45)"""
    def login(self):
        user=self.username.get().strip()
        pas=self.password.get().strip()

        if not user or not pas:
            tk.messagebox.showwarning("Campos vacíos", "Por favor, llene todos los campos.")
            return

        resultado = self.controller.validacion(user, pas)
            
        if resultado:
            self.controller.show_frame(Ventas)  # Reemplaza Principal con la pantalla que deseas mostrar después del login
        else:
            tk.messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# --- CLASE REGISTRO ---
class Registro(PantallaBase):
    def __init__(self, padre, controller):
        super().__init__(padre, controller)
        self.widgets()

    def widgets(self):
        self.crear_fondo_comun()
        
        # Cuadro un poco más alto para que quepan los 3 campos
        frame_reg = tk.Frame(self, bg="#FFFFFF", highlightbackground="#D3D3D3", highlightthickness=1)
        frame_reg.place(x=400, y=70, width=400, height=560)

        tk.Label(frame_reg, text="CREAR CUENTA", font="arial 16 bold", bg="white", fg="#333333").place(x=70, y=40)

        # 1. Nuevo Usuario
        self.lbl_u = tk.Label(frame_reg, text="Nuevo Usuario", font="arial 12", bg="white", fg="gray")
        self.lbl_u.place(x=70, y=120)
        self.ent_u = tk.Entry(frame_reg, font="arial 14", bd=0, highlightthickness=1, highlightbackground="lightgray")
        self.ent_u.place(x=70, y=120, width=260, height=35)
        self.configurar_animacion(self.ent_u, self.lbl_u, 95, 120)

        # 2. Nueva Contraseña
        self.lbl_p = tk.Label(frame_reg, text="Nueva Contraseña", font="arial 12", bg="white", fg="gray")
        self.lbl_p.place(x=70, y=200)
        self.ent_p = tk.Entry(frame_reg, font="arial 14", bd=0, highlightthickness=1, highlightbackground="lightgray", show="*")
        self.ent_p.place(x=70, y=200, width=260, height=35)
        self.configurar_animacion(self.ent_p, self.lbl_p, 175, 200)

        # 3. Código de Registro (Tu campo especial)
        self.lbl_k = tk.Label(frame_reg, text="Código de Registro", font="arial 12", bg="white", fg="gray")
        self.lbl_k.place(x=70, y=280)
        self.ent_k = tk.Entry(frame_reg, font="arial 14", bd=0, highlightthickness=1, highlightbackground="lightgray", show="*")
        self.ent_k.place(x=70, y=280, width=260, height=35)
        self.configurar_animacion(self.ent_k, self.lbl_k, 255, 280)

        # Botón para registrar
        tk.Button(frame_reg, text="CONFIRMAR REGISTRO", bg="#4CAF50", fg="white", font="arial 12 bold", bd=0, cursor="hand2").place(x=70, y=360, width=260, height=45)

        # Botón para regresar si ya tienes cuenta
        tk.Button(frame_reg, text="¿Ya tienes cuenta? Inicia sesión", font="arial 10", bg="white", fg="#2196F3", bd=0, cursor="hand2",
                  command=lambda: self.controller.show_frame(Login)).place(x=70, y=430, width=260)
