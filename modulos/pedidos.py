from tkinter import *
import csv
from tkinter import ttk,messagebox,filedialog
import tkinter as tk
import especialidades.controlador as ctrl

class Pedidos(tk.Frame):
    def __init__(self,padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def cargar_proveedores(self, event=None):
        proveedores=ctrl.obtener_nombres_proveedores()
        self.entry_proveedor['values']=proveedores

    def filtrar_proveedores(self, event=None):
        texto_buscado = self.entry_proveedor.get().lower().strip()
        
        todos_los_proveedores = ctrl.obtener_nombres_proveedores()
        
        if texto_buscado == "":
            self.entry_proveedor['values'] = todos_los_proveedores
        else:
            proveedores_filtrados = [
                prov for prov in todos_los_proveedores 
                if texto_buscado in str(prov).lower()
            ]
            
            self.entry_proveedor['values'] = proveedores_filtrados

    def widgets(self):
        labelframe=LabelFrame(self,text="Pedidos",font="arial 20 bold",bg="#C6D9E3")
        labelframe.place(x=20,y=20,width=400,height=200)

        lavel_proveedor=Label(labelframe,text="Proveedor:",font="arial 14 bold",bg="#C6D9E3")
        lavel_proveedor.place(x=10,y=10)
        self.entry_proveedor=ttk.Combobox(labelframe,font="arial 14 bold")
        self.entry_proveedor.bind("<<ComboboxSelected>>", self.cargar_proveedores)
        self.entry_proveedor.place(x=110,y=10,width=200,height=40)
        self.cargar_proveedores()
        self.entry_proveedor.bind("<<KeyRelease>>", self.filtrar_proveedores)
        
        """self.btn_confirmar = tk.Button(
            labelframe, text="Confirmar y Generar Orden",
            font="arial 12 bold", bg="#4CAF50", fg="white", cursor="hand2",
            command=self.procesar_y_exportar_pedido
        )
        self.btn_confirmar.place(x=520, y=15, width=250, height=40)"""
        
        tk.Label(labelframe, text="Formato Exportación:", font="arial 10 bold", bg="#C6D9E3").place(x=460, y=0)
        
        self.formato_var = tk.StringVar(value="Ambos (PDF y CSV)")
        self.combo_formato = ttk.Combobox(labelframe, textvariable=self.formato_var, values=["PDF", "CSV", "Ambos (PDF y CSV)"], state="readonly", font="arial 10")
        self.combo_formato.place(x=460, y=25, width=150, height=30)

        self.btn_confirmar = tk.Button(
            labelframe, text="Confirmar Pedido", 
            font="arial 11 bold", bg="#4CAF50", fg="white", cursor="hand2",
            command=self.procesar_y_exportar_pedido
        )
        self.btn_confirmar.place(x=620, y=15, width=160, height=45)

        self.canvas_frame = tk.Frame(self, bg="#FFFFFF", bd=2, relief="groove")
        self.canvas_frame.place(x=20, y=140, width=800, height=460)
        
        self.canvas=tk.Canvas(self.canvas_frame, bg="#FFFFFF")
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.frame_articulos_scroll= tk.Frame(self.canvas, bg="#FFFFFF")
        
        self.frame_articulos_scroll.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0,0), window=self.frame_articulos_scroll, anchor="nw", width=770)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
    
    def cargar_catalogo_pedido(self, event=None):
        proveedor_seleccionado = self.entry_proveedor.get()
        if not proveedor_seleccionado or "-" not in proveedor_seleccionado:
            return

        id_proveedor = proveedor_seleccionado.split("-")[0].strip() 
        
        for widget in self.frame_articulos_scroll.winfo_children():
            widget.destroy()
        
        fila_header = tk.Frame(self.frame_articulos_scroll, bg="#9FB8C7", pady=5)
        fila_header.pack(fill="x", padx=10, pady=5)
        tk.Label(fila_header, text="Producto / Artículo", font=("arial", 12, "bold"), bg="#9FB8C7", width=30, anchor="w").pack(side="left", padx=5)
        tk.Label(fila_header, text="Costo ($)", font=("arial", 12, "bold"), bg="#9FB8C7", width=10).pack(side="left")
        tk.Label(fila_header, text="Stock Actual", font=("arial", 12, "bold"), bg="#9FB8C7", width=10).pack(side="left")
        tk.Label(fila_header, text="Cantidad a Pedir", font=("arial", 12, "bold"), bg="#9FB8C7", width=15).pack(side="right", padx=10)

        self.lista_productos = ctrl.obtener_catalogo_por_proveedor(id_proveedor)
        self.entradas_cantidad = {}

        for idx, prod in enumerate(self.lista_productos):
            id_p, nombre, costo, precio, stock = prod
            bg_color = "#F0F4F8" if idx % 2 == 0 else "#FFFFFF"
            
            fila_frame = tk.Frame(self.frame_articulos_scroll, bg=bg_color, pady=5)
            fila_frame.pack(fill="x", padx=10, pady=2)
            
            tk.Label(fila_frame, text=nombre, font=("arial", 11), bg=bg_color, width=30, anchor="w").pack(side="left", padx=5)
            tk.Label(fila_frame, text=f"${costo:.2f}", font=("arial", 11), bg=bg_color, width=10).pack(side="left")
            tk.Label(fila_frame, text=str(stock), font=("arial", 11), bg=bg_color, width=10).pack(side="left")
            
            frame_selector = tk.Frame(fila_frame, bg=bg_color)
            frame_selector.pack(side="right", padx=15)

            entry_cant = tk.Entry(frame_selector, font=("arial", 12, "bold"), width=4, justify="center", relief="solid", bd=1)
            entry_cant.insert(0, "0")

            def cambiar_cantidad(entry, delta):
                try:
                    val = int(entry.get())
                except ValueError:
                    val = 0
                nuevo = val + delta
                if nuevo < 0: nuevo = 0
                entry.delete(0, tk.END)
                entry.insert(0, str(nuevo))
            
            btn_menos=tk.Button(frame_selector, text="-", font=("arial", 12, "bold"), width=2, bg="#FFCDD2", cursor="hand2", command=lambda e=entry_cant: cambiar_cantidad(e, -1))
            btn_menos.pack(side="left", padx=2)
            
            entry_cant.pack(side="left", padx=5)
            
            btn_mas = tk.Button(frame_selector, text="+", font=("arial", 12, "bold"), width=2, bg="#C8E6C9", cursor="hand2", command=lambda e=entry_cant: cambiar_cantidad(e, 1))
            btn_mas.pack(side="left", padx=2)

            self.entradas_cantidad[id_p]= {
                "entry": entry_cant,
                "nombre": nombre,
                "costo": costo
            }

    def procesar_y_exportar_pedido(self):
        proveedor_sel = self.entry_proveedor.get()
        if not proveedor_sel or "-" not in proveedor_sel:
            messagebox.showwarning("Error", "Seleccione un proveedor válido primero.")
            return

        id_proveedor = proveedor_sel.split("-")[0].strip()
        nombre_proveedor = proveedor_sel.split("-")[1].strip()

        productos_pedidos = []
        total_general = 0
        
        for id_p, info in self.entradas_cantidad.items():
            try:
                cantidad = int(info["entry"].get().strip())
            except ValueError:
                cantidad = 0 

            if cantidad > 0:
                productos_pedidos.append({
                    "nombre": info["nombre"],
                    "cantidad": cantidad,
                    "costo": info["costo"]
                })
                total_general += cantidad * float(info["costo"])
                
        if not productos_pedidos:
            messagebox.showwarning("Pedido Vacío", "Use los botones [+] para seleccionar cantidades antes de confirmar.")
            return

        # NOTA: Aquí irá la validación de fondos cuando se implemente el módulo de Finanzas.
        
        exito, msj = ctrl.guardar_pedido_bd(id_proveedor, productos_pedidos)
        if not exito:
            messagebox.showerror("Error de Base de Datos", msj)
            return

        formato = self.combo_formato.get()
        mensajes_rutas = []
        
        try:
            if "PDF" in formato or "Ambos" in formato:
                ruta_pdf = ctrl.generar_orden_pedido_pdf(nombre_proveedor, productos_pedidos, total_general)
                mensajes_rutas.append(f"• PDF: {ruta_pdf}")
                
            if "CSV" in formato or "Ambos" in formato:
                ruta_csv = ctrl.generar_csv_pedido(nombre_proveedor, productos_pedidos, total_general)
                mensajes_rutas.append(f"• CSV: {ruta_csv}")
                
            rutas_str = "\n".join(mensajes_rutas)
            messagebox.showinfo("Confirmado", f"{msj}\n\nArchivos generados en Descargas:\n{rutas_str}")
            
            self.entry_proveedor.set("")
            for widget in self.frame_articulos_scroll.winfo_children():
                widget.destroy()
            self.entradas_cantidad.clear()
            
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"Pedido guardado en BD, pero falló la exportación: {e}")

    """def cargar_catalogo_pedido(self, event=None):
    
        id_proveedor = self.entry_proveedor.get().split("-")[0].strip() 
        
        for widget in self.frame_articulos_scroll.winfo_children():
            widget.destroy()

        self.lista_productos = ctrl.obtener_catalogo_por_proveedor(id_proveedor)
        self.entradas_cantidad = {} 

        for idx, prod in enumerate(self.lista_productos):
            id_p, nombre, costo, precio, stock = prod
            
            fila_frame = tk.Frame(self.frame_articulos_scroll, bg="#F0F4F8", pady=5)
            fila_frame.pack(fill="x", padx=10, pady=2)
            
            tk.Label(fila_frame, text=nombre, font=("arial", 11), bg="#F0F4F8", width=30, anchor="w").pack(side="left")
            tk.Label(fila_frame, text=f"${costo}", font=("arial", 11), bg="#F0F4F8", width=10).pack(side="left")
            tk.Label(fila_frame, text=f"Stock: {stock}", font=("arial", 11), bg="#F0F4F8", width=10).pack(side="left")
            
            entry_cant = tk.Entry(fila_frame, font=("arial", 11), width=8, justify="center")
            entry_cant.pack(side="right", padx=10)
            entry_cant.insert(0, "0") 
            
            self.entradas_cantidad[id_p] = {
                "entry": entry_cant,
                "nombre": nombre,
                "costo": costo
            }
"""