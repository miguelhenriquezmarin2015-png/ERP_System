from tkinter import *
import csv
from tkinter import ttk,messagebox,filedialog
import tkinter as tk
import especialidades.controlador as ctrl

class Pedidos(tk.Frame):
    def __init__(self,padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.lbl_total_orden = None
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
        
        labelframe = LabelFrame(self, text="Pedidos", font="arial 20 bold", bg="#C6D9E3")
        labelframe.place(x=20, y=20, width=400, height=200)

        lavel_proveedor = Label(labelframe, text="Proveedor:", font="arial 14 bold", bg="#C6D9E3")
        lavel_proveedor.place(x=10, y=10)
        
        self.entry_proveedor = ttk.Combobox(labelframe, font="arial 14 bold")
        self.entry_proveedor.place(x=110, y=10, width=200, height=40)

        tk.Label(labelframe, text="Formato Exportación:", font="arial 10 bold", bg="#C6D9E3").place(x=460, y=0)
        
        self.formato_var = tk.StringVar(value="Ambos (PDF y CSV)")
        self.combo_formato = ttk.Combobox(labelframe, textvariable=self.formato_var, values=["PDF", "CSV", "Ambos (PDF y CSV)"])
        self.combo_formato.place(x=460, y=25, width=150, height=30)

        self.canvas_frame = tk.Frame(self, bg="#FFFFFF", bd=2, relief="groove")
        self.canvas_frame.place(x=20, y=140, width=800, height=400)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.frame_articulos_scroll = tk.Frame(self.canvas, bg="#FFFFFF")

        self.frame_articulos_scroll.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.frame_articulos_scroll, anchor="nw", width=770)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        frame_acciones_externo = tk.Frame(self, bg="#C6D9E3")
        frame_acciones_externo.place(x=20, y=555, width=800, height=50)

        self.lbl_total_orden = tk.Label(
            frame_acciones_externo, text="Total Estimado: $0.00", 
            font=("arial", 14, "bold"), bg="#C6D9E3", fg="black"
        )
        self.lbl_total_orden.pack(side="left", padx=5, pady=5)

        self.btn_confirmar = tk.Button(
            frame_acciones_externo, text="Confirmar Pedido",
            font="arial 11 bold", bg="#4CAF50", fg="white", cursor="hand2", bd=0,
            padx=15, pady=6, command=self.procesar_y_exportar_pedido
        )
        self.btn_confirmar.pack(side="right", padx=5, pady=5)

        self.entry_proveedor.bind("<<ComboboxSelected>>", self.cargar_catalogo_pedido)
        self.entry_proveedor.bind("<KeyRelease>", self.filtrar_proveedores)
        self.cargar_proveedores()
    
    def cargar_catalogo_pedido(self, event=None):
        for widget in self.frame_articulos_scroll.winfo_children():
            widget.destroy()

        proveedor_sel = self.entry_proveedor.get().strip()
        
        if not proveedor_sel:
            return
        proveedor_sel = self.entry_proveedor.get().strip()
        if not proveedor_sel:
            return

        for widget in self.frame_articulos_scroll.winfo_children():
            widget.destroy()

        frame_header = tk.Frame(self.frame_articulos_scroll, bg="#ECEFF1", height=30)
        frame_header.pack(fill="x", padx=5, pady=(2, 5))

        headers = [("Producto / Artículo", 28), ("Costo Prov.", 12), ("Inv. Actual", 12), ("Acomprar", 15)]
        for text, width in headers:
            anchor_val = "w" if text == "Producto / Artículo" else "center"
            lbl_h = tk.Label(frame_header, text=text, font=("arial", 11, "bold"), bg="#ECEFF1", width=width, anchor=anchor_val)
            
            if text == "Acomprar":
                lbl_h.pack(side="right", padx=25)
            else:
                lbl_h.pack(side="left", padx=5)

        articulos = ctrl.obtener_catalogo_por_proveedor(proveedor_sel)
        
        self.items_pedido = {} 

        for idx, prod in enumerate(articulos):
            id_p, nombre, costo, precio, stock = prod
            color_fila = "#F8F9FA" if idx % 2 == 0 else "white"

            fila = tk.Frame(self.frame_articulos_scroll, bg=color_fila, pady=6)
            fila.pack(fill="x", pady=1)

            lbl_nom = tk.Label(fila, text=f"{nombre}", font=("arial", 11), bg=color_fila, width=28, anchor="w")
            lbl_nom.pack(side="left", padx=5)
            
            lbl_cos = tk.Label(fila, text=f"${float(costo):.2f}", font=("arial", 11), bg=color_fila, width=12, anchor="center")
            lbl_cos.pack(side="left", padx=5)
            
            lbl_stk = tk.Label(fila, text=f"{stock} uds", font=("arial", 11), bg=color_fila, width=12, anchor="center")
            lbl_stk.pack(side="left", padx=5)

            frame_control = tk.Frame(fila, bg=color_fila)
            frame_control.pack(side="right", padx=25)

            entry_cant = tk.Entry(frame_control, font=("arial", 10, "bold"), width=4, justify="center")
            entry_cant.bind("<KeyRelease>", lambda e: self.recalcular_total_pedido())
            entry_cant.insert(0, "0")

            def cambiar_cantidad(operacion, entry=entry_cant):
                try:
                    actual = int(entry.get())
                except ValueError:
                    actual = 0
                nuevo = max(0, actual + 1 if operacion == "+" else actual - 1)
                entry.delete(0, tk.END)
                entry.insert(0, str(nuevo))
                
                self.recalcular_total_pedido()

            btn_menos = tk.Button(frame_control, text="-", font=("arial", 9, "bold"), width=2, bg="#CFD8DC", command=lambda e=entry_cant: cambiar_cantidad("-", e))
            btn_mas = tk.Button(frame_control, text="+", font=("arial", 9, "bold"), width=2, bg="#B0BEC5", command=lambda e=entry_cant: cambiar_cantidad("+", e))

            btn_menos.pack(side="left", padx=2)
            entry_cant.pack(side="left", padx=2)
            btn_mas.pack(side="left", padx=2)

            self.items_pedido[id_p] = {"entry": entry_cant, "nombre": nombre, "costo": float(costo)}

        self.recalcular_total_pedido()

    def procesar_y_exportar_pedido(self):
        proveedor_sel = self.entry_proveedor.get()
        if not proveedor_sel or "-" not in proveedor_sel:
            messagebox.showwarning("Error", "Seleccione un proveedor válido primero.")
            return

        id_proveedor = proveedor_sel.split("-")[0].strip()
        nombre_proveedor = proveedor_sel.split("-")[1].strip()

        productos_pedidos = []
        total_general = 0

        for id_p, info in self.items_pedido.items():
            try:
                cantidad = int(info["entry"].get().strip())
            except ValueError:
                cantidad = 0

            if cantidad > 0:
                costo_unitario = float(info["costo"])
                total_fila = cantidad * costo_unitario
                total_general += total_fila
                
                productos_pedidos.append({
                    "id": id_p,
                    "nombre": info["nombre"],
                    "cantidad": cantidad,
                    "costo": costo_unitario,
                    "total": total_fila
                })

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

            if "csv" in formato or "Ambos" in formato:
                ruta_csv = ctrl.generar_csv_pedido(nombre_proveedor, productos_pedidos, total_general)
                mensajes_rutas.append(f"• CSV: {ruta_csv}")

            rutas_str = "\n".join(mensajes_rutas)
            messagebox.showinfo("Confirmado", f"{msj}\n\nArchivos generados en Descargas:\n{rutas_str}")
        
            self.items_pedido.clear() 

            self.entry_proveedor.set("") 

            self.cargar_catalogo_pedido()

            self.recalcular_total_pedido()

        except Exception as e:
            messagebox.showerror("Error de Exportación", f"Pedido guardado en BD, pero falló la exportación: {e}")

    def recalcular_total_pedido(self):
        total_acumulado = 0.0
        for id_p, info in self.items_pedido.items():
            try:
                cant = int(info["entry"].get().strip())
            except ValueError:
                cant = 0
                
            total_acumulado += cant * info["costo"]
        
        if self.lbl_total_orden:
            self.lbl_total_orden.config(text=f"Total Estimado: ${total_acumulado:.2f}")

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