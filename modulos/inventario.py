from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox,filedialog
import especialidades.controlador as ctrl

class Inventario(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.filtro_bajo_stock_activo = False
        self.widgets()
        self.bind("<FocusIn>", lambda event: self.cargar_articulos() if event.widget == self else None)

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
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollbar_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.window_id, width=e.width))
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
        
        self.bt3=tk.Button(lblframe_botones,text="INVENTARIO BAJO",font="arial 12 bold",bg="#4CAF50",fg="white",command=self.alternar_filtro_stock)
        self.bt3.place(x=10,y=20,width=250,height=40)

        self.bt2=tk.Button(lblframe_botones,text="Limpiar Busqueda",font="arial 12 bold",bg="#2196F3",fg="white",command=self.limpiar_formulario_inventario)
        self.bt2.place(x=10,y=80,width=250,height=40)

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
            
        if datos is not None:
            articulos = datos
        else:
            articulos = ctrl.obtener_articulos()
            
        headers = ["ID", "Nombre", "Costo", "Precio", "Stock", "Vencimiento", "Acción"]
        for col_idx, text in enumerate(headers):
            lbl_header = tk.Label(
                self.scrollbar_frame,
                text=text,
                font=("arial", 16, "bold"),
                bg="#9FB8C7",
                fg="black",
                relief="groove",
                padx=10,
                pady=5,
                anchor="center"
            )
            lbl_header.grid(row=0, column=col_idx, sticky="nsew")
            
        if not articulos:
            for i, w in enumerate([1, 5, 2, 2, 2, 3, 1]):
                self.scrollbar_frame.grid_columnconfigure(i, weight=w)
            return
            
        for row_idx, art in enumerate(articulos, start=1):
            color_fila = "#E1EBF0" if row_idx % 2 == 0 else "#F4F8FA"
            
            id_art = art[0] if len(art) > 0 else None
            nombre = art[1] if len(art) > 1 else "Sin Nombre"
            costo = art[2] if len(art) > 2 else 0.0
            precio = art[3] if len(art) > 3 else 0.0
            stock = art[4] if len(art) > 4 else 0
            perecedero = art[5] if len(art) > 5 else 0
            vencimiento = art[6] if len(art) > 6 else None
            
            if perecedero == 1:
                texto_vence = vencimiento if vencimiento else "Sin Fecha"
                color_letras = "#D32F2F"
            else:
                texto_vence = "No Aplica"
                color_letras = "black"
                
            valores_fila = [id_art, nombre, f"${float(costo):,.2f}", f"${float(precio):,.2f}", stock, texto_vence]
            
            for col_idx, valor in enumerate(valores_fila):
                lbl_dato = tk.Label(
                    self.scrollbar_frame,
                    text=valor,
                    font=("arial", 16),
                    bg=color_fila,
                    fg=color_letras if col_idx == 5 else "black",
                    relief="groove",
                    anchor="w" if col_idx == 1 else ("e" if col_idx in [2, 3, 4] else "center"),
                    padx=10,
                    pady=5
                )
                lbl_dato.grid(row=row_idx, column=col_idx, sticky="nsew")
                
            btn_eliminar = tk.Button(
                self.scrollbar_frame,
                text="Borrar",
                bg="#F44336",
                fg="white",
                font=("arial", 11, "bold"),
                cursor="hand2",
                command=lambda id_a=id_art, nom=nombre: self.borrar_articulo(id_a, nom)
            )
            btn_eliminar.grid(row=row_idx, column=6, sticky="nsew", padx=5, pady=2)
            
        self.scrollbar_frame.grid_columnconfigure(0, weight=1)  # ID
        self.scrollbar_frame.grid_columnconfigure(1, weight=5)  # Nombre
        self.scrollbar_frame.grid_columnconfigure(2, weight=2)  # Costo
        self.scrollbar_frame.grid_columnconfigure(3, weight=2)  # Precio
        self.scrollbar_frame.grid_columnconfigure(4, weight=2)  # Stock
        self.scrollbar_frame.grid_columnconfigure(5, weight=3)  # Vencimiento
        self.scrollbar_frame.grid_columnconfigure(6, weight=1)  # Acción
        
        def refrescar_dimensiones_reales():
            if hasattr(self, 'canvas') and hasattr(self, 'window_id'):
                self.scrollbar_frame.update_idletasks()
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))
                ancho_canvas = self.canvas.winfo_width()
                if ancho_canvas > 1:
                    self.canvas.itemconfig(self.window_id, width=ancho_canvas)
                    
        self.after(10, refrescar_dimensiones_reales)

    def verificar_alertas_stock(self):
        productos_bajos = ctrl.mostrar_inventario_baja_cantidad()
        
        if productos_bajos:
            mensaje = "⚠️ ALERTA DE STOCK BAJO ⚠️\n\nLos siguientes artículos tienen menos de 15 unidades:\n\n"
            for id_art, nombre, costo, precio, stock, perecedero, vencimiento in productos_bajos:
                mensaje += f"• {nombre}: ({stock} unidades restantes)\n"
                
            messagebox.showwarning("Control de Inventario", mensaje)

    def verificar_alertas_vencimiento(self):
        productos_vencidos = ctrl.obtener_productos_por_vencer()
        
        if productos_vencidos:
            mensaje = "🚨 ALERTA DE CADUCIDAD 🚨\n\nLos siguientes productos perecederos vencerán pronto:\n\n"
            for nombre, fecha in productos_vencidos:
                mensaje += f"• {nombre}: Vence el {fecha}\n"
                
            messagebox.showwarning("Alerta de Sanidad / Inventario", mensaje)

    def al_abrir_pestana_inventario(self):
        self.cargar_articulos() 
        
        self.verificar_alertas_stock()
        self.verificar_alertas_vencimiento()
    
    def borrar_articulo(self, id_articulo, nombre_articulo):
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de que deseas eliminar permanentemente el artículo '{nombre_articulo}'?\nEsta acción no se puede deshacer."
        )
        if respuesta:
            try:
                ctrl.eliminar_articulo(id_articulo)
                messagebox.showinfo("Eliminado", f"{nombre_articulo} ha sido eliminado")
                
                self.cargar_articulos()   
                
            except Exception as e:
                messagebox.showerror("Error", f"{nombre_articulo} no se pudo eliminar:\n{e}")

    def limpiar_formulario_inventario(self):
        self.combobox_buscar.delete(0, tk.END)
        
        if hasattr(self, 'cargar_articulos'):
            self.cargar_articulos()