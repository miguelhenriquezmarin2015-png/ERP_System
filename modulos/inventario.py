from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox,filedialog
import modulos.controlador as ctrl

class Inventario(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.filtro_bajo_stock_activo = False
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

        self.combobox_buscar=ttk.Entry(frame_buscar,font="arial 12",)
        self.combobox_buscar.place(x=10,y=5,width=250,height=40 )
        self.combobox_buscar.bind("<KeyRelease>", self.buscar_articulo)
        self.cargar_articulos()
#obsiones
        lblframe_botones=LabelFrame(self,text="OPCIONES",font="arial 14 bold",bg="#C6D9E3")
        lblframe_botones.place(x=10,y=250,width=280,height=260)

        bt1=tk.Button(lblframe_botones,text="AGREGAR",font="arial 12 bold",bg="#4CAF50",fg="white",command=self.agregar_articulo)
        bt1.place(x=10,y=10,width=250,height=40)

        bt2=tk.Button(lblframe_botones,text="EDITAR",font="arial 12 bold",bg="#2196F3",fg="white", command=self.editar_producto)
        bt2.place(x=10,y=60,width=250,height=40)
        
        self.bt3=tk.Button(lblframe_botones,text="INVENTARIO BAJO",font="arial 12 bold",bg="#F44336",fg="white",command=self.alternar_filtro_stock)
        self.bt3.place(x=10,y=110,width=250,height=40)

        bt4=tk.Button(lblframe_botones,text="ELIMINAR",font="arial 12 bold",bg="#BA48D6",fg="white",command=self.eliminar_producto)
        bt4.place(x=10,y=160,width=250,height=40)

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

        costo=tk.Label(top,text="Costo:",font="arial 12 bold",bg="#C6D9E3")
        costo.place(x=20,y=55,width=80,height=25)
        entry_costo=tk.Entry(top,font="arial 12")
        entry_costo.place(x=110,y=55,width=250,height=25)

        precio=tk.Label(top,text="Precio:",font="arial 12 bold",bg="#C6D9E3")
        precio.place(x=20,y=90,width=80,height=25)
        entry_precio=tk.Entry(top,font="arial 12")
        entry_precio.place(x=110,y=90,width=250,height=25)

        stock=tk.Label(top,text="Stock:",font="arial 12 bold",bg="#C6D9E3")
        stock.place(x=20,y=125,width=80,height=25)
        entry_stock=tk.Entry(top,font="arial 12")
        entry_stock.place(x=110,y=125,width=250,height=25)

        def guardar():
            producto=entry_producto.get()
            costo=entry_costo.get()
            precio=entry_precio.get()
            stock=entry_stock.get()

            if not producto or not costo or not precio or not stock:
                messagebox.showerror("Error", "todos los campos deben ser llenados")
                return
            
            try:
                costo=float(costo)
                precio=float(precio)
                stock=int(stock)
                ctrl.guardar_articulo(producto,costo,precio,stock)
                messagebox.showinfo("Exito","Producto agregado correctamente")
                self.cargar_articulos()
                top.destroy()
            except ValueError:
                messagebox.showerror("Error","costo, precio y stock deben ser numeros validos" )
        
        tk.Button(top,text="Guardar",font="arial 12 bold",command=guardar).place(x=40, y=200,width=130,height=40)
        tk.Button(top,text="Cancelar",font="arial 12 bold",command=top.destroy).place(x=240, y=200,width=130,height=40)

    def alternar_filtro_stock(self):
        if not self.filtro_bajo_stock_activo:
            productos_bajos = ctrl.mostrar_inventario_baja_cantidad()
            
            if not productos_bajos:
                messagebox.showinfo("Inventario Sano", "No hay productos con stock menor a 15 unidades.")
                return
                
            self.cargar_articulos(productos_bajos)
            
            self.bt3.config(text="MOSTRAR TODO", bg="#9FB8C7")
            
            self.filtro_bajo_stock_activo = True
            
        else:
            self.cargar_articulos()
            self.bt3.config(text="VER BAJO STOCK", bg="#F44336")            
            self.filtro_bajo_stock_activo = False


    def buscar_articulo(self, event=None):
        if self.filtro_bajo_stock_activo:
            self.bt3.config(text="VER BAJO STOCK", bg="#FFC107")
            self.filtro_bajo_stock_activo = False
            
        nombre = self.combobox_buscar.get()
        resultado = ctrl.buscar_articulo(nombre)
        self.cargar_articulos(resultado)

    def cargar_articulos(self, datos=None):
        for widget in self.scrollbar_frame.winfo_children():
            widget.destroy()
            
        headers = ["ID", "Nombre","Costo", "Precio", "Stock"]
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
            articulos = datos 
        else:
            articulos = ctrl.obtener_articulos() 

        for row_idx, art in enumerate(articulos, start=1):
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

        self.scrollbar_frame.grid_columnconfigure(0, weight=1)
        self.scrollbar_frame.grid_columnconfigure(1, weight=5)
        self.scrollbar_frame.grid_columnconfigure(2, weight=2)
        self.scrollbar_frame.grid_columnconfigure(3, weight=2)
        self.scrollbar_frame.grid_columnconfigure(4, weight=2)
    
    def editar_producto(self):
        texto_buscado = self.combobox_buscar.get().strip()
        
        if not texto_buscado:
            messagebox.showerror("Error", "Escribe al menos una parte del nombre del producto a editar.")
            return
            
        productos_encontrados = ctrl.buscar_articulo(texto_buscado)
        
        if not productos_encontrados:
            messagebox.showerror("Error", f"No se encontró ningún producto que coincida con '{texto_buscado}'.")
            return
            
        producto_exacto = productos_encontrados[0]
        
        id_prod, nombre_producto, costo_prod, pre_prod, st_prod = producto_exacto

        vent_editar = tk.Toplevel(self)
        vent_editar.title(f"Editar: {nombre_producto}")
        vent_editar.geometry("400x300+150+50")
        vent_editar.configure(bg="#C6D9E3")
        vent_editar.resizable(False, False)
        
        tk.Label(vent_editar, text="Nombre:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=30)
        ent_nombre = tk.Entry(vent_editar, font="arial 12")
        ent_nombre.place(x=120, y=30, width=220)
        ent_nombre.insert(0, nombre_producto)

        tk.Label(vent_editar, text="Costo:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=60)
        ent_costo = tk.Entry(vent_editar, font="arial 12")
        ent_costo.place(x=120, y=60, width=220)
        ent_costo.insert(0, str(costo_prod))

        tk.Label(vent_editar, text="Precio:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=80)
        ent_precio = tk.Entry(vent_editar, font="arial 12")
        ent_precio.place(x=120, y=80, width=220)
        ent_precio.insert(0, str(pre_prod)) 

        tk.Label(vent_editar, text="Stock:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=130)
        ent_stock = tk.Entry(vent_editar, font="arial 12")
        ent_stock.place(x=120, y=130, width=220)
        ent_stock.insert(0, str(st_prod)) 

        def guardar_cambios():
            nuevo_nom = ent_nombre.get().strip()
            nuevo_costo = ent_costo.get().strip()
            nuevo_pre = ent_precio.get().strip()
            nuevo_st = ent_stock.get().strip()
            
            if not nuevo_nom or not nuevo_costo or not nuevo_pre or not nuevo_st:
                messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=vent_editar)
                return
                
            try:
                ctrl.actualizar_articulo(id_prod, nuevo_nom, float(nuevo_costo), float(nuevo_pre), int(nuevo_st))
                messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
                
                vent_editar.destroy()      # Cierra la ventana flotante
                self.cargar_articulos()    # Recarga la tabla de inmediato
                
            except ValueError:
                messagebox.showerror("Error", "Costo, Precio o Stock inválidos. Ingresa números válidos.", parent=vent_editar)

        btn_guardar = tk.Button(
            vent_editar, 
            text="GUARDAR CAMBIOS", 
            font="arial 12 bold", 
            bg="#9FB8C7", 
            command=guardar_cambios
        )
        btn_guardar.place(x=100, y=200, width=200, height=40)
    
    def eliminar_producto(self):
        texto_buscado = self.combobox_buscar.get().strip()

        if not texto_buscado:
            messagebox.showerror(
                "Error",
                "Escribe al menos una parte del nombre del producto a eliminar.",
            )
            return

        productos_encontrados = ctrl.buscar_articulo(texto_buscado)

        if not productos_encontrados:
            messagebox.showerror(
                "Error",
                f"No se encontró ningún producto que coincida con '{texto_buscado}'.",
            )
            return

        producto_exacto = productos_encontrados[0]
        id_prod, nom_prod,costo_prod, pre_prod, st_prod = producto_exacto

        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de que deseas eliminar permanentemente el producto '{nom_prod}'?",
        )

        if confirmacion:
            try:
                ctrl.eliminar_articulo(id_prod)
                messagebox.showinfo("Éxito", f"Producto '{nom_prod}' eliminado.")

                self.combobox_buscar.delete(0, tk.END)
                self.cargar_articulos()

            except Exception as e:
                messagebox.showerror(
                    "Error", f"No se pudo eliminar el artículo: {e}"
                )