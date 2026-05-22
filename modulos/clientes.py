from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
import modulos.controlador as ctrl 
import threading

class Clientes(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def cargar_clientes(self, datos=None):
        for widget in self.scrollbar_frame.winfo_children():
            widget.destroy()

        headers = ["ID", "Nombre", "Cédula", "Teléfono", "Tipo"]
        for col_idx, text in enumerate(headers):
            lbl_header = tk.Label(
                self.scrollbar_frame,
                text=text,
                font=("arial", 16, "bold"),
                bg="#9FB8C7",
                fg="black",
                relief="groove",
                padx=10,
                pady=5
            )
            lbl_header.grid(row=0, column=col_idx, sticky="nsew")

        if datos is not None:
            clientes = datos
        else:
            clientes = ctrl.obtener_clientes()

        for row_idx, clie in enumerate(clientes, start=1):
            color_fila = "#E1EBF0" if row_idx % 2 == 0 else "#F4F8FA"

            for col_idx, valor in enumerate(clie):
                lbl_dato = tk.Label(
                    self.scrollbar_frame,
                    text=valor,
                    font=("arial", 16),
                    bg=color_fila,
                    anchor="center" if col_idx in [0, 2, 4] else "w",
                    padx=10,
                    pady=5
                )
                lbl_dato.grid(row=row_idx, column=col_idx, sticky="nsew")

                lbl_dato.bind("<Button-1>", lambda event, datos=clie: self.seleccionar_cliente(datos))

        self.scrollbar_frame.grid_columnconfigure(0, weight=1)
        self.scrollbar_frame.grid_columnconfigure(1, weight=5)
        self.scrollbar_frame.grid_columnconfigure(2, weight=2)
        self.scrollbar_frame.grid_columnconfigure(3, weight=2)
        self.scrollbar_frame.grid_columnconfigure(4, weight=2)

    def seleccionar_cliente(self, datos_cliente):
        
        
        self.entry_nombre.delete(0, tk.END)
        self.entry_cedula.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        
        # 2. Rellenar con la información correspondiente usando los índices correctos
        self.entry_nombre.insert(0, datos_cliente[1])    
        self.entry_cedula.insert(0, datos_cliente[2])     
        self.entry_telefono.insert(0, datos_cliente[3])  
        
        if datos_cliente[4] == "Natural":                 
            self.entry_tipo.current(0)
        else:
            self.entry_tipo.current(1)
            
        self.id_cliente_seleccionado = datos_cliente[0] 


    def cargar_datos_clientes(self):
        for fila in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(fila)
        lista_clientes = ctrl.obtener_clientes() 
        
        for i, cliente in enumerate(lista_clientes):
            # Determinar si la fila es par o impar para el color de fondo
            tag_color = "fila_par" if i % 2 == 0 else "fila_impar"
            
            self.tabla_clientes.insert("", tk.END, values=cliente, tags=(tag_color,))

    def widgets(self):
        canvas_clientes=tk.Label(self,text="Clientes",font="arial 20 bold",bg="#C6D9E3")
        canvas_clientes.place(x=300,y=20,width=890,height=625)

        self.canvas=tk.Canvas(canvas_clientes)
        self.scrollbar=Scrollbar(canvas_clientes,orient="vertical",command=self.canvas.yview)
        self.scrollbar_frame=tk.Frame(self.canvas,bg="#C6D9E3")
        self.scrollbar_frame.bind(
            "<Configure>"
            ,lambda e: self.canvas.configure
            (scrollregion=self.canvas.bbox("all")
             )
        )
        self.canvas.bind("<Configure>"
                         ,lambda e: self.canvas.itemconfig(self.canvas.find_withtag("all")[0],width=e.width))
        self.canvas.create_window((0,0),window=self.scrollbar_frame,anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left",fill="both",expand=True)
        self.scrollbar.pack(side="right",fill="y")

#agregar clientes
        frame_agregar=LabelFrame(self,text="Clientes",font="arial 12 bold",bg="#C6D9E3")
        frame_agregar.place(x=20,y=20,width=250,height=480)

        self.label_nombre=tk.Label(frame_agregar,text="Nombre",font="arial 12 bold",bg="#C6D9E3")
        self.label_nombre.place(x=5,y=5,width=220,height=40)

        self.entry_nombre=tk.Entry(frame_agregar,font="arial 12 bold")
        self.entry_nombre.place(x=5,y=45,width=220,height=40)

        self.label_cedula=tk.Label(frame_agregar,text="Cedula",font="arial 12 bold",bg="#C6D9E3")
        self.label_cedula.place(x=5,y=90,width=220,height=40)
        self.entry_cedula=tk.Entry(frame_agregar,font="arial 12 bold")
        self.entry_cedula.place(x=5,y=130,width=220,height=40)

        self.label_telefono=tk.Label(frame_agregar,text="Telefono",font="arial 12 bold",bg="#C6D9E3")
        self.label_telefono.place(x=5,y=180,width=220,height=40)
        self.entry_telefono=tk.Entry(frame_agregar,font="arial 12 bold")
        self.entry_telefono.place(x=5,y=220,width=220,height=40)

        self.label_tipo=tk.Label(frame_agregar,text="Tipo",font="arial 12 bold",bg="#C6D9E3")
        self.label_tipo.place(x=5,y=270,width=220,height=40)
        estilo_combo = ttk.Style()
        estilo_combo.configure("TCombobox", fieldbackground="white", background="white")
        self.entry_tipo = ttk.Combobox(frame_agregar, values=["Natural", "Jurídica"], font="arial 12 bold", state="readonly")
        self.entry_tipo.place(x=5, y=310, width=220, height=40)
        self.entry_tipo.current(0)

#obsiones

        lblframa_botones=LabelFrame(self,text="Opciones",font="arial 12 bold",bg="#C6D9E3")
        lblframa_botones.place(x=20,y=500,width=250,height=140)

        bt1=tk.Button(lblframa_botones,text="Agregar",font="arial 12 bold",bg="#4CAF50",fg="white",command=self.nuevo_cliente)
        bt1.place(x=10,y=10,width=220,height=40)

        bt2=tk.Button(lblframa_botones,text="Modificar",font="arial 12 bold",bg="#2196F3",fg="white",command=self.actualizar_cliente)
        bt2.place(x=10,y=60,width=220,height=40)

        self.cargar_clientes()

    def nuevo_cliente(self):
        nom = self.entry_nombre.get()
        tel = self.entry_telefono.get()
        ced = self.entry_cedula.get()
        tip = self.entry_tipo.get()     

        if nom == "" or ced == "" or tip == "":
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        ctrl.guardar_cliente(nom, tel, ced, tip)

        messagebox.showinfo("Éxito", f"¡Cliente '{nom}' agregado correctamente!")

        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_cedula.delete(0, tk.END)
        self.entry_tipo.current(0) 

        self.cargar_clientes()
       
    def actualizar_cliente(self):
        if not hasattr(self, 'id_cliente_seleccionado') or self.id_cliente_seleccionado is None:
            messagebox.showwarning("Atención", "Por favor, selecciona primero un cliente de la lista para modificar.")
            return

        nom = self.entry_nombre.get()
        tel = self.entry_telefono.get()
        ced = self.entry_cedula.get()
        tip = self.entry_tipo.get()

        if nom == "" or ced == "":
            messagebox.showwarning("Atención", "El Nombre y la Cédula no pueden estar vacíos.")
            return

        ctrl.modificar_cliente(self.id_cliente_seleccionado, nom, tel, ced, tip)

        messagebox.showinfo("Éxito", f"¡Cliente '{nom}' actualizado correctamente!")

        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_cedula.delete(0, tk.END)
        self.entry_tipo.current(0)
        self.id_cliente_seleccionado = None

        self.cargar_clientes()



        