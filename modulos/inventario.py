#import controler
from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox,filedialog
import modulos.controlador as ctrl

class Inventario(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def widgets(self):
        canvas_articulos=tk.Label(self,text="ARTICULOS",font="arial 20 bold",bg="#C6D9E3")
        canvas_articulos.place(x=300,y=20,width=880,height=600)

        self.canvas=tk.Canvas(canvas_articulos)
        self.scrollbar=Scrollbar(canvas_articulos,orient="vertical",command=self.canvas.yview)
        self.scrollbar_frame=tk.Frame(self.canvas,bg="#C6D9E3")
        self.scrollbar_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.bind(
            "<Configure>", 
            lambda e: self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=e.width)
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
        self.combobox_buscar.bind("<<ComboboxSelected>>",self.buscar_articulo)
        self.combobox_buscar.bind("<KeyRelease>", self.buscar_articulo)
        self.cargar_articulos()

#obsiones
        lblframe_botones=LabelFrame(self,text="OPCIONES",font="arial 14 bold",bg="#C6D9E3")
        lblframe_botones.place(x=10,y=250,width=280,height=180)

        bt1=tk.Button(lblframe_botones,text="AGREGAR",font="arial 12 bold",bg="#9FB8C7",fg="black",command=self.agregar_articulo)
        bt1.place(x=10,y=10,width=250,height=40)

        bt2=tk.Button(lblframe_botones,text="EDITAR",font="arial 12 bold",bg="#9FB8C7",fg="black")
        bt2.place(x=10,y=50,width=250,height=40)

        bt3=tk.Button(lblframe_botones,text="ELIMINAR",font="arial 12 bold",bg="#9FB8C7",fg="black")
        bt3.place(x=10,y=90,width=250,height=40)
    
    def agregar_articulo(self):
        top=tk.Toplevel(self)
        top.title("Agregar Producto")
        top.geometry("400x300+150+50")
        top.configure(bg="#C6D9E3")
        top.resizable(False,False)

        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        producto=tk.Label(top,text="Producto:",font="arial 12 bold",bg="#C6D9E3")
        producto.place(x=20,y=20,width=80,height=25)
        entry_producto=tk.Entry(top,font="arial 12")
        entry_producto.place(x=110,y=20,width=250,height=25)

        precio=tk.Label(top,text="Precio:",font="arial 12 bold",bg="#C6D9E3")
        precio.place(x=20,y=55,width=80,height=25)
        entry_precio=tk.Entry(top,font="arial 12")
        entry_precio.place(x=110,y=55,width=250,height=25)

        stock=tk.Label(top,text="Stock:",font="arial 12 bold",bg="#C6D9E3")
        stock.place(x=20,y=90,width=80,height=25)
        entry_stock=tk.Entry(top,font="arial 12")
        entry_stock.place(x=110,y=90,width=250,height=25)

        def guardar():
            producto=entry_producto.get()
            precio=entry_precio.get()
            stock=entry_stock.get()

            if not producto or not precio or not stock:
                messagebox.showerror("Error", "todos los campos deben ser llenados")
                return
            
            try:
                precio=float(precio)
                stock=int(stock)
                ctrl.guardar_articulo(producto,precio,stock)
                messagebox.showinfo("Exito","Producto agregado correctamente")
                self.cargar_articulos()
                top.destroy()
            except ValueError:
                messagebox.showerror("Error","precio y stock deben ser numeros validos" )
        
        tk.Button(top,text="Guardar",font="arial 12 bold",command=guardar).place(x=40, y=200,width=130,height=40)
        tk.Button(top,text="Cancelar",font="arial 12 bold",command=top.destroy).place(x=240, y=200,width=130,height=40)

    def buscar_articulo(self,event=None):
        nombre=self.combobox_buscar.get()
        resultado=ctrl.buscar_articulo(nombre)
        self.cargar_articulos(resultado)

    def cargar_articulos(self, datos=None):
    # 1. Limpiar todos los elementos visuales previos en el frame
        for widget in self.scrollbar_frame.winfo_children():
            widget.destroy()
            
        # 2. Dibujar los encabezados de la tabla
        headers = ["ID", "Nombre", "Precio", "Stock"]
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
            
        # 3. COMBINACIÓN: Determinar el origen de los productos
        if datos is not None:
            articulos = datos  # Si viene de la búsqueda ("pasta")
        else:
            articulos = ctrl.obtener_articulos()  # Carga inicial de todo el inventario

        # 4. Dibujar las filas de datos con tu efecto cebra
        for row_idx, art in enumerate(articulos, start=1):
            # Alterna colores de fondo para facilitar la lectura
            color_fila = "#E1EBF0" if row_idx % 2 == 0 else "#F4F8FA"
            
            for col_idx, valor in enumerate(art):
                lbl_dato = tk.Label(
                    self.scrollbar_frame,
                    text=valor,
                    font=("arial", 16),
                    bg=color_fila,
                    anchor="w",
                    padx=10,
                    pady=5
                )
                lbl_dato.grid(row=row_idx, column=col_idx, sticky="nsew")

        # 5. EL RESTO DE LA FUNCIÓN: Configurar el comportamiento elástico de las columnas
        self.scrollbar_frame.grid_columnconfigure(0, weight=1)
        self.scrollbar_frame.grid_columnconfigure(1, weight=5)
        self.scrollbar_frame.grid_columnconfigure(2, weight=2)
        self.scrollbar_frame.grid_columnconfigure(3, weight=2)
