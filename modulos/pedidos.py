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
        self.bind("<FocusIn>", self.al_recuperar_foco)

    def al_recuperar_foco(self, event=None):
        if event and event.widget != self:
            return
            
        if hasattr(self, 'todos_los_proveedores'):
            del self.todos_los_proveedores

        self.cargar_proveedores()

    def cargar_proveedores(self, event=None):
        proveedores=ctrl.obtener_nombres_proveedores()
        self.entry_proveedor['values']=proveedores

    def filtrar_proveedores(self, event=None):
        texto_buscado = self.entry_proveedor.get().lower().strip()
        
        self.todos_los_proveedores = ctrl.obtener_nombres_proveedores()
        
        if texto_buscado == "":
            self.entry_proveedor['values'] = self.todos_los_proveedores
        else:
            proveedores_filtrados = [
                prov for prov in self.todos_los_proveedores
                if texto_buscado in str(prov).lower()
            ]
            self.entry_proveedor['values'] = proveedores_filtrados

    def programar_filtrado(self, event=None):
        if hasattr(self, '_timer_id') and self._timer_id:
            self.after_cancel(self._timer_id)
        
        self._timer_id = self.after(1500, self.ejecutar_filtro_y_abrir)

    def ejecutar_filtro_y_abrir(self):
        self.filtrar_proveedores()
        self.entry_proveedor.event_generate("<Down>")

    def widgets(self):
        
        labelframe = LabelFrame(self, text="Pedidos", font="arial 20 bold", bg="#C6D9E3")
        labelframe.place(x=20, y=20, width=1160, height=100)

        lavel_proveedor = Label(labelframe, text="Proveedor:", font="arial 14 bold", bg="#C6D9E3")
        lavel_proveedor.place(x=10, y=10)
        
        self.entry_proveedor = ttk.Combobox(labelframe, font="arial 14 bold")
        self.entry_proveedor.place(x=130, y=10, width=200, height=40)
        self.entry_proveedor.bind("<KeyRelease>", self.programar_filtrado)

        tk.Label(labelframe, text="Formato del reporte:", font="arial 14 bold", bg="#C6D9E3").place(x=370, y=10)
        
        self.formato_var = tk.StringVar(value="Ambos (PDF y CSV)")
        self.combo_formato = ttk.Combobox(labelframe, textvariable=self.formato_var, values=["PDF", "CSV", "Ambos (PDF y CSV)"])
        self.combo_formato.place(x=590, y=10, width=180, height=40)

        # ver saldo
        self.saldo_var = tk.StringVar()
        saldo_actual = ctrl.obtener_saldo_fondo("Fondo Reposición") 
        if isinstance(saldo_actual, tuple) and saldo_actual:
            saldo_num = float(saldo_actual[0])
        elif saldo_actual is not None:
            saldo_num = float(saldo_actual)
        else:
            saldo_num = 0.00
        self.saldo_var.set(f"Saldo Fondo Reposición: ${saldo_num:,.2f}")

        self.label_saldo = tk.Label(labelframe, textvariable=self.saldo_var, font="arial 14 bold", bg="#C6D9E3")
        self.label_saldo.place(x=810, y=10)

        self.canvas_frame = tk.Frame(self, bg="#FFFFFF", bd=2, relief="groove")
        self.canvas_frame.place(x=20, y=150, width=1160, height=400)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.frame_articulos_scroll = tk.Frame(self.canvas, bg="#FFFFFF")

        self.frame_articulos_scroll.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.frame_articulos_scroll, anchor="nw", width=1130)
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

        self.btn_limpiar = tk.Button(
            frame_acciones_externo, text="Limpiar Selección",
            font="arial 11 bold", bg="#f44336", fg="white", cursor="hand2", bd=0,
            padx=15, pady=6, command=self.limpiar_formulario_pedidos
        )
        self.btn_limpiar.pack(side="right", padx=5, pady=5)

        self.entry_proveedor.bind("<<ComboboxSelected>>", self.cargar_catalogo_pedido)
        self.entry_proveedor.bind("<KeyRelease>", self.programar_filtrado)
        self.cargar_proveedores()
    
    def cargar_catalogo_pedido(self, event=None):
        for widget in self.frame_articulos_scroll.winfo_children():
            widget.destroy()

        proveedor_sel = self.entry_proveedor.get().strip()
        if not proveedor_sel:
            return

        frame_header = tk.Frame(self.frame_articulos_scroll, bg="#ECEFF1", height=35)
        frame_header.pack(fill="x", padx=5, pady=(2, 5))
        frame_header.pack_propagate(False)  

        headers_config = [
            ("Producto / Artículo", "w"),
            ("Costo Prov.", "center"),
            ("Inv. Actual", "center")
        ]

        for text, anchor_val in headers_config:
            lbl_h = tk.Label(frame_header, text=text, font=("arial", 11, "bold"), bg="#ECEFF1", anchor=anchor_val)
            lbl_h.pack(side="left", padx=15, expand=True, fill="both")

        lbl_acomprar = tk.Label(frame_header, text="Acomprar", font=("arial", 11, "bold"), bg="#ECEFF1", anchor="center")
        lbl_acomprar.pack(side="right", padx=35)


        articulos = ctrl.obtener_catalogo_por_proveedor(proveedor_sel)
        self.items_pedido = {}

        if not articulos:
            return

        for idx, prod in enumerate(articulos):
            id_p, nombre, costo, precio, stock = prod
            color_fila = "#F8F9FA" if idx % 2 == 0 else "white"
            
            fila = tk.Frame(self.frame_articulos_scroll, bg=color_fila, height=40)
            fila.pack(side="top", fill="x", expand=True, padx=5, pady=2)
            fila.pack_propagate(False)  
                        
            lbl_nom = tk.Label(fila, text=f"{nombre}", font=("arial", 11), bg=color_fila, anchor="w")
            lbl_nom.pack(side="left", padx=15, expand=True, fill="both")
            
            lbl_cos = tk.Label(fila, text=f"${float(costo):.2f}", font=("arial", 11), bg=color_fila, anchor="center")
            lbl_cos.pack(side="left", padx=5, expand=True, fill="both")
            
            lbl_stk = tk.Label(fila, text=f"{stock} uds", font=("arial", 11), bg=color_fila, anchor="center")
            lbl_stk.pack(side="left", padx=5, expand=True, fill="both")
            
            frame_control = tk.Frame(fila, bg=color_fila)
            frame_control.pack(side="right", padx=35, fill="y")
            
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

            btn_menos = tk.Button(
                frame_control, text="-", font=("arial", 9, "bold"), width=2, bg="#CFD8DC", 
                command=lambda: cambiar_cantidad("-")
            )
            btn_mas = tk.Button(
                frame_control, text="+", font=("arial", 9, "bold"), width=2, bg="#B0BEC5", 
                command=lambda: cambiar_cantidad("+")
            )
            
            btn_menos.pack(side="left", padx=2)
            entry_cant.pack(side="left", padx=2, expand=True, fill="y")
            btn_mas.pack(side="left", padx=2)
            
            self.items_pedido[id_p] = {"entry": entry_cant, "nombre": nombre, "costo": float(costo)}

        self.recalcular_total_pedido()
        
        self.frame_articulos_scroll.update_idletasks()
        if hasattr(self, 'canvas'):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            self.canvas.yview_moveto(0)

    def limpiar_formulario_pedidos(self):
        self.entry_proveedor.set("")
        if hasattr(self, 'todos_los_proveedores'):
            del self.todos_los_proveedores
            
        if hasattr(self, 'items_pedido'):
            for entry in self.items_pedido.values():
                entry["entry"].delete(0, tk.END)
                entry["entry"].insert(0, "0")
                
        if hasattr(self, 'recalcular_total_pedido'):
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

        # VALIDACIÓN DE FONDOS (Plan de Acción)
        saldo_reposicion = ctrl.obtener_saldo_fondo("Fondo de Reposición")
        if total_general > saldo_reposicion:
            messagebox.showwarning(
                "Fondos Insuficientes", 
                f"El costo total de este pedido (${total_general:.2f}) supera el presupuesto asignado en el 'Fondo de Reposición' (${saldo_reposicion:.2f}).\n\nPor favor, asigne capital a este fondo desde el módulo de Finanzas antes de emitir la orden."
            )
            return

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
        
            self.items_pedido.clear() 

            self.entry_proveedor.set("") 

            self.cargar_catalogo_pedido()

            self.recalcular_total_pedido()

        except Exception as e:
            messagebox.showerror("Error de Exportación", f"Pedido guardado en BD, pero falló la exportación: {e}")

    def recalcular_total_pedido(self):
        if not hasattr(self, 'items_pedido') or self.items_pedido is None:
            return 
        total_acumulado = 0.0
        for id_p, info in self.items_pedido.items():
            try:
                cant = int(info["entry"].get().strip())
            except ValueError:
                cant = 0
                
            total_acumulado += cant * info["costo"]
        
        if self.lbl_total_orden:
            self.lbl_total_orden.config(text=f"Total Estimado: ${total_acumulado:.2f}")

    def refrescar_saldo(self):
        nuevo_saldo = ctrl.obtener_saldo()
        
        if isinstance(nuevo_saldo, tuple) and nuevo_saldo:
            saldo_num = float(nuevo_saldo[0]) 
        elif nuevo_saldo is not None:
            saldo_num = float(nuevo_saldo)
        else:
            saldo_num = 0.00
        self.saldo_var.set(f"Saldo Fondo Reposición: ${saldo_num:,.2f}")

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