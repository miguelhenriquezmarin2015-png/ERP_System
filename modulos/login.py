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
     import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Login(tk.Frame):
    def __init__(self, padre, controller):
        super().__init__(padre)
        self.controller = controller
        self.widgets()

    def widgets(self):
       import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Login(tk.Frame):
    def __init__(self, padre, controller):
        super().__init__(padre)
        self.controller = controller
        self.widgets()

    def widgets(self):
        # --- FONDO E IMAGEN ---
        # Contenedor para la imagen de fondo
        fondo = tk.Frame(self, bg="#C6D9E3")
        fondo.place(x=0, y=0, width=1200, height=700)

        try:
            self.bg_imagen = Image.open("imagenes/login.jpg")
            self.bg_imagen = self.bg_imagen.resize((1200, 700))
            self.bg_imagen = ImageTk.PhotoImage(self.bg_imagen)
            self.bg_label = tk.Label(fondo, image=self.bg_imagen)
            self.bg_label.place(x=0, y=0, width=1200, height=700)
        except:
            print("No se encontró la imagen de fondo")

        # --- CUADRO CENTRAL BLANCO ---
        # Nota: Tkinter estándar no tiene bordes redondeados nativos, 
        # pero este diseño limpio ayuda mucho.
        self.frame1 = tk.Frame(self, bg="#FFFFFF", highlightbackground="#D3D3D3", highlightthickness=1)
        self.frame1.place(x=400, y=100, width=400, height=500)

        # --- SECCIÓN USUARIO ---
        # El Label y el Entry comparten la misma 'y' inicial (220)
        self.user_label = tk.Label(self.frame1, text="Nombre de Usuario", font="arial 12", bg="#FFFFFF", fg="gray")
        self.user_label.place(x=70, y=200) 

        self.username = tk.Entry(self.frame1, font="arial 14", bd=0, highlightthickness=1, highlightbackground="lightgray")
        self.username.place(x=70, y=200, width=260, height=35)
        
        # IMPORTANTE: Traer al frente para que se vea al abrir
        self.user_label.lift() 

        # --- SECCIÓN CONTRASEÑA ---
        self.pass_label = tk.Label(self.frame1, text="Contraseña", font="arial 12", bg="#FFFFFF", fg="gray")
        self.pass_label.place(x=70, y=280)

        self.password = tk.Entry(self.frame1, font="arial 14", bd=0, highlightthickness=1, highlightbackground="lightgray", show="*")
        self.password.place(x=70, y=280, width=260, height=35)
        
        self.pass_label.lift()

        # --- BOTÓN ENTRAR ---
        self.btn_entrar = tk.Button(self.frame1, text="INICIAR SESIÓN", bg="#2196F3", fg="white", 
                                   font="arial 12 bold", cursor="hand2", bd=0, activebackground="#1976D2", activeforeground="white")
        self.btn_entrar.place(x=70, y=380, width=260, height=45)

        self.btn_registro = tk.Button(self.frame1, text="REGISTRARSE", bg="#4CAF50", fg="white", 
                                   font="arial 12 bold", cursor="hand2", bd=0, activebackground="#388E3C", activeforeground="white")
        self.btn_registro.place(x=70, y=430, width=260, height=45)

        # --- EVENTOS (BINDS) ---
        # Estos detectan cuando haces clic dentro o fuera del cuadro
        self.username.bind("<FocusIn>", lambda e: self.subir_animacion(self.user_label, 175))
        self.username.bind("<FocusOut>", lambda e: self.bajar_animacion(self.user_label, self.username, 200))
        
        self.password.bind("<FocusIn>", lambda e: self.subir_animacion(self.pass_label, 255))
        self.password.bind("<FocusOut>", lambda e: self.bajar_animacion(self.pass_label, self.password, 280))

        # Truco extra: Si haces clic en el texto, también activa el Entry
        self.user_label.bind("<Button-1>", lambda e: self.username.focus_set())
        self.pass_label.bind("<Button-1>", lambda e: self.password.focus_set())

    # --- FUNCIONES DE ANIMACIÓN ---
    def subir_animacion(self, label, nueva_y):
        label.place(y=nueva_y)
        label.config(font=("arial", 10, "bold"), fg="#2196F3")
        # No hace falta lift aquí porque al subir ya no choca con el Entry

    def bajar_animacion(self, label, entry, y_original):
        if not entry.get(): # Solo si el cuadro está vacío
            label.place(y=y_original)
            label.config(font=("arial", 12), fg="gray")
            label.lift() # Lo ponemos al frente de nuevo para que sea visible

class Registro(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def widgets(self):
         # --- FONDO E IMAGEN ---
        # Contenedor para la imagen de fondo
        fondo = tk.Frame(self, bg="#C6D9E3")
        fondo.place(x=0, y=0, width=1200, height=700)

        try:
            self.bg_imagen = Image.open("imagenes/login.jpg")
            self.bg_imagen = self.bg_imagen.resize((1200, 700))
            self.bg_imagen = ImageTk.PhotoImage(self.bg_imagen)
            self.bg_label = tk.Label(fondo, image=self.bg_imagen)
            self.bg_label.place(x=0, y=0, width=1200, height=700)
        except:
            print("No se encontró la imagen de fondo")

        # --- CUADRO CENTRAL BLANCO ---
        # Nota: Tkinter estándar no tiene bordes redondeados nativos, 
        # pero este diseño limpio ayuda mucho.
        self.frame1 = tk.Frame(self, bg="#FFFFFF", highlightbackground="#D3D3D3", highlightthickness=1)
        self.frame1.place(x=400, y=100, width=400, height=500)

        # --- SECCIÓN USUARIO ---
        # El Label y el Entry comparten la misma 'y' inicial (220)
        self.user_label = tk.Label(self.frame1, text="Nombre de Usuario", font="arial 12 bold", bg="#FFFFFF", fg="gray")
        self.user_label.place(x=70, y=200) 

        self.username = tk.Entry(self.frame1, font="arial 14", bd=0, highlightthickness=1, highlightbackground="lightgray")
        self.username.place(x=70, y=200, width=260, height=35)
        
        # IMPORTANTE: Traer al frente para que se vea al abrir
        self.user_label.lift() 

        # --- SECCIÓN CONTRASEÑA ---
        self.pass_label = tk.Label(self.frame1, text="Contraseña", font="arial 12 bold", bg="#FFFFFF", fg="gray")
        self.pass_label.place(x=70, y=280)

        self.password = tk.Entry(self.frame1, font="arial 14", bd=0, highlightthickness=1, highlightbackground="lightgray", show="*")
        self.password.place(x=70, y=280, width=260, height=35)
        
        self.pass_label.lift()

        key=tk.Label(self.frame1,text="Codigo de Registro",font="arial 12 bold",bg="#FFFFFF",fg="gray")
        key.place(x=70, y=320)
        self.key=tk.Entry(self.frame1,font="arial 14",bd=0,highlightthickness=1,highlightbackground="lightgray",show="*")
        self.key.place(x=70, y=320, width=260, height=35)

        # --- BOTÓN ENTRAR ---
        self.btn_entrar = tk.Button(self.frame1, text="INICIAR SESIÓN", bg="#2196F3", fg="white", 
                                   font="arial 12 bold", cursor="hand2", bd=0, activebackground="#1976D2", activeforeground="white")
        self.btn_entrar.place(x=70, y=380, width=260, height=45)

        self.btn_registro = tk.Button(self.frame1, text="REGISTRARSE", bg="#4CAF50", fg="white", 
                                   font="arial 12 bold", cursor="hand2", bd=0, activebackground="#388E3C", activeforeground="white")
        self.btn_registro.place(x=70, y=430, width=260, height=45)

        # --- EVENTOS (BINDS) ---
        # Estos detectan cuando haces clic dentro o fuera del cuadro
        self.username.bind("<FocusIn>", lambda e: self.subir_animacion(self.user_label, 175))
        self.username.bind("<FocusOut>", lambda e: self.bajar_animacion(self.user_label, self.username, 200))
        
        self.password.bind("<FocusIn>", lambda e: self.subir_animacion(self.pass_label, 255))
        self.password.bind("<FocusOut>", lambda e: self.bajar_animacion(self.pass_label, self.password, 280))

        # Truco extra: Si haces clic en el texto, también activa el Entry
        self.user_label.bind("<Button-1>", lambda e: self.username.focus_set())
        self.pass_label.bind("<Button-1>", lambda e: self.password.focus_set())

    # --- FUNCIONES DE ANIMACIÓN ---
    def subir_animacion(self, label, nueva_y):
        label.place(y=nueva_y)
        label.config(font=("arial", 10, "bold"), fg="#2196F3")
        # No hace falta lift aquí porque al subir ya no choca con el Entry

    def bajar_animacion(self, label, entry, y_original):
        if not entry.get(): # Solo si el cuadro está vacío
            label.place(y=y_original)
            label.config(font=("arial", 12), fg="gray")
            label.lift() # Lo ponemos al frente de nuevo para que sea visible