from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
import especialidades.controlador as ctrl
import threading

class Proveedor(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.id_proveedor_seleccionado=None
        self.widgets()

    def widgets(self):
        
        canvas_proveedor=tk.Label(self,text="Proveedores",font="arial 20 bold",bg="#C6D9E3")
        canvas_proveedor.place(x=280,y=20,width=915,height=625)

        self.canvas=tk.Canvas(canvas_proveedor)
        self.scrollbar=Scrollbar(canvas_proveedor,orient="vertical",command=self.canvas.yview)
        self.scrollbar_frame=tk.Frame(self.canvas,bg="#C6D9E3")
        self.scrollbar_frame.bind(
            "<Configure>"
            ,lambda e: self.canvas.configure
            (scrollregion=self.canvas.bbox("all")
             )
        )
        self.canvas.bind("<Configure>",lambda e: self.canvas.itemconfig(self.canvas.find_withtag("all")[0],width=e.width))
        self.canvas.create_window((0,0),window=self.scrollbar_frame,anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left",fill="both",expand=True)
        self.scrollbar.pack(side="right",fill="y")

#obsiones

        labelproveedor = tk.LabelFrame(self, text="Nuevo Proveedor", font="arial 16 bold", bg="#C6D9E3")
        labelproveedor.place(x=20, y=20, width=250, height=600)

        label_nombre = tk.Label(labelproveedor, text="Nombre: ", font="arial 14 bold", bg="#C6D9E3")
        label_nombre.place(x=10, y=10)
        self.entry_nombre = tk.Entry(labelproveedor, font="arial 14")
        self.entry_nombre.place(x=10, y=60, width=230, height=30)

        label_rif = tk.Label(labelproveedor, text="RIF: ", font="arial 14 bold", bg="#C6D9E3")
        label_rif.place(x=10, y=100)
        self.entry_rif = tk.Entry(labelproveedor, font="arial 14")
        self.entry_rif.place(x=10, y=140, width=230, height=30)

        label_contacto = tk.Label(labelproveedor, text="Contacto: ", font="arial 14 bold", bg="#C6D9E3")
        label_contacto.place(x=10, y=190)
        self.entry_contacto = tk.Entry(labelproveedor, font="arial 14")
        self.entry_contacto.place(x=10, y=230, width=230, height=30)

        self.boton_modificar = tk.Button(labelproveedor, text="Actualizar", font="arial 14 bold", bg="#4CAF50", fg="white", command=self.modificar_proveedor_ui)
        self.boton_modificar.place(x=10, y=310, width=230, height=40)

        self.boton_limpiar = tk.Button(labelproveedor, text="Limpiar", font="arial 14 bold", bg="#2196F3", fg="white", command=self.limpiar_formulario_proveedor)
        self.boton_limpiar.place(x=10, y=360, width=230, height=40)

        self.boton_guardar = tk.Button(labelproveedor, text="Guardar", font="arial 14 bold", bg="#BA48D6", fg="white",command=self.guardar_nuevo_proveedor)
        self.boton_guardar.place(x=10, y=420, width=230, height=40)

        self.boton_eliminar = tk.Button(labelproveedor, text="Eliminar", font="arial 14 bold", bg="#F44336", fg="white", command=self.eliminar_proveedor_ui)
        self.boton_eliminar.place(x=10, y=470, width=230, height=40)

        self.cargar_proveedores()

    def cargar_proveedores(self):
        if not hasattr(self, 'scrollbar_frame') or not self.scrollbar_frame.winfo_exists():
            return

        for widget in self.scrollbar_frame.winfo_children():
            widget.destroy()

        headers = ["ID", "Nombre de Empresa", "RIF", "Contacto / Teléfono", "Perfil / Opciones"]
        for col_idx, text in enumerate(headers):
            lbl = tk.Label(
                self.scrollbar_frame,
                text=text, 
                font=("arial", 16, "bold"), 
                bg="#9FB8C7", 
                fg="black", 
                relief="groove", 
                padx=10, 
                pady=5
            )
            lbl.grid(row=0, column=col_idx, sticky="nsew")

        lista_proveedores = ctrl.obtener_proveedores()

        for row_idx, prov in enumerate(lista_proveedores, start=1):
            id_prov, nombre, rif, contacto = prov
            color_fila = "#E1EBF0" if row_idx % 2 == 0 else "#F4F4F4"

            valores = [id_prov, nombre, rif, contacto]

            for col_idx, valor in enumerate(valores):
                lbl_dato = tk.Label(
                    self.scrollbar_frame, 
                    text=valor, 
                    font=("arial", 16), 
                    bg=color_fila, 
                    fg="black", 
                    relief="groove",
                    anchor="w" if col_idx == 1 else "center", 
                    padx=10, 
                    pady=5
                )
                lbl_dato.grid(row=row_idx, column=col_idx, sticky="nsew")
                lbl_dato.bind("<Button-1>", lambda event, datos=prov: self.seleccionar_proveedor(datos))

            frame_acciones = tk.Frame(self.scrollbar_frame, bg=color_fila, relief="groove", bd=1)
            frame_acciones.grid(row=row_idx, column=4, sticky="nsew")

            def desplegar_menu(b=None, p=prov, id_p=id_prov):
                menu_popup = tk.Menu(btn_opciones, tearoff=0, font=("arial", 10), bg="white", fg="black", activebackground="#2196F3")
                
                menu_popup.add_command(label="📁 Catálogo", command=lambda: self.ver_catalogo_articulos(p))
                menu_popup.add_command(label="💳 Compras", command=lambda: self.ver_historial_compras(id_p))
                menu_popup.add_command(label="⏳ Pendientes", command=lambda: self.ver_pedidos_pendientes(id_p))
                
                x = btn_opciones.winfo_rootx()
                y = btn_opciones.winfo_rooty() + btn_opciones.winfo_height()
                menu_popup.post(x, y)

            btn_opciones = tk.Button(
                frame_acciones,
                text="Opciones ▾",
                bg="#4A5568", fg="white",
                font=("arial", 10, "bold"), bd=0, cursor="hand2",
                command=desplegar_menu 
            )
            btn_opciones.pack(side="left", padx=10, pady=5, expand=True)

        self.scrollbar_frame.grid_columnconfigure(0, weight=1)
        self.scrollbar_frame.grid_columnconfigure(1, weight=4) 
        self.scrollbar_frame.grid_columnconfigure(2, weight=2) 
        self.scrollbar_frame.grid_columnconfigure(3, weight=2) 
        self.scrollbar_frame.grid_columnconfigure(4, weight=4) 

    def guardar_nuevo_proveedor(self):
        nom = self.entry_nombre.get().strip()
        rif = self.entry_rif.get().strip()
        tel = self.entry_contacto.get().strip()

        if not nom or not rif or not tel:
            messagebox.showerror("Error", "Todos los campos principales son obligatorios.")
            return

        exito, mensaje = ctrl.registrar_proveedor_db(nom, rif, tel)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.entry_nombre.delete(0, tk.END)
            self.entry_rif.delete(0, tk.END)
            self.entry_contacto.delete(0, tk.END)
            self.cargar_proveedores()
        else:
            messagebox.showerror("Error", mensaje)

    def ver_catalogo_articulos(self, datos_proveedor):
        id_prov = datos_proveedor
        nombre_prov = datos_proveedor

        # Crear ventana flotante
        top_cat = tk.Toplevel(self)
        top_cat.title(f"Catálogo del Proveedor: {nombre_prov}")
        top_cat.geometry("1100x550")
        top_cat.resizable(False, False)
        top_cat.grab_set()

        top_cat.controller = self.controller
        control_edicion = {"id_articulo": None}

        frame_tabla_sub = tk.LabelFrame(top_cat, text="Artículos en Catálogo", font=("arial", 11, "bold"))
        frame_tabla_sub.place(x=320, y=10, width=760, height=520)

        canvas_sub = tk.Canvas(frame_tabla_sub, bg="white", highlightthickness=0)
        scrollbar_sub = ttk.Scrollbar(frame_tabla_sub, orient="vertical", command=canvas_sub.yview)
        frame_grid_sub = tk.Frame(canvas_sub, bg="white")

        frame_grid_sub.bind("<Configure>", lambda e: canvas_sub.configure(scrollregion=canvas_sub.bbox("all")))
        canvas_sub.create_window((0, 0), window=frame_grid_sub, anchor="nw")
        canvas_sub.configure(yscrollcommand=scrollbar_sub.set)

        canvas_sub.place(x=10, y=10, width=720, height=480)
        scrollbar_sub.place(x=735, y=10, width=15, height=480)

        def refrescar_subtabla():
            for widget in frame_grid_sub.winfo_children():
                widget.destroy()

            headers = ["ID", "Nombre", "Costo", "Precio", "Stock", "Vencimiento", "Acciones"]
            for col_idx, h_text in enumerate(headers):
                lbl = tk.Label(frame_grid_sub, text=h_text, font=("arial", 10, "bold"), relief="groove", padx=5, pady=5)
                lbl.grid(row=0, column=col_idx, sticky="nsew")

            productos = ctrl.obtener_catalogo_por_proveedor(id_prov)
            if not productos:
                return

            for r_idx, prod in enumerate(productos, start=1):
                color_f = "#F5F5F5" if r_idx % 2 == 0 else "white"
                
                id_p = prod[0] if len(prod) > 0 else None
                nom = prod[1] if len(prod) > 1 else "Sin Nombre"
                cos = prod[2] if len(prod) > 2 else 0.0
                pre = prod[3] if len(prod) > 3 else 0.0
                stk = prod[4] if len(prod) > 4 else 0
                per = prod[5] if len(prod) > 5 else 0
                venc = prod[6] if len(prod) > 6 else None

                venc_text = venc if (per == 1 and venc) else ("Sin Fecha" if per == 1 else "No Aplica")

                valores = [id_p, nom, f"${float(cos):.2f}", f"${float(pre):.2f}", stk, venc_text]
                for c_idx, val in enumerate(valores):
                    lbl_d = tk.Label(frame_grid_sub, text=val, font=("arial", 10), bg=color_f, relief="groove", padx=5, pady=5)
                    lbl_d.grid(row=r_idx, column=c_idx, sticky="nsew")

                btn_ed = tk.Button(
                    frame_grid_sub, text="Editar", bg="#2196F3", fg="white", font=("arial", 9, "bold"),
                    command=lambda p=prod: preparar_edicion(p)
                )
                btn_ed.grid(row=r_idx, column=6, sticky="nsew", padx=2, pady=2)

            frame_grid_sub.grid_columnconfigure(0, weight=1)  # ID
            frame_grid_sub.grid_columnconfigure(1, weight=4)  # Nombre
            frame_grid_sub.grid_columnconfigure(2, weight=2)  # Costo
            frame_grid_sub.grid_columnconfigure(3, weight=2)  # Precio
            frame_grid_sub.grid_columnconfigure(4, weight=1)  # Stock
            frame_grid_sub.grid_columnconfigure(5, weight=3)  # Vencimiento
            frame_grid_sub.grid_columnconfigure(6, weight=2)  # Acciones

            frame_grid_sub.update_idletasks()
            canvas_sub.configure(scrollregion=canvas_sub.bbox("all"))

        frame_add = tk.LabelFrame(top_cat, text="Gestionar Artículo", font=("arial", 11, "bold"))
        frame_add.place(x=10, y=10, width=300, height=520)

        tk.Label(frame_add, text="Nombre del Producto:", font=("arial", 10)).place(x=10, y=10)
        ent_nom = tk.Entry(frame_add, font=("arial", 10))
        ent_nom.place(x=10, y=30, width=260)

        tk.Label(frame_add, text="Costo de Compra ($):", font=("arial", 10)).place(x=10, y=60)
        ent_cos = tk.Entry(frame_add, font=("arial", 10))
        ent_cos.place(x=10, y=80, width=260)

        tk.Label(frame_add, text="Precio de Venta ($):", font=("arial", 10)).place(x=10, y=110)
        ent_pre = tk.Entry(frame_add, font=("arial", 10))
        ent_pre.place(x=10, y=130, width=260)

        tk.Label(frame_add, text="¿Es Perecedero?", font=("arial", 10)).place(x=10, y=160)
        combo_per = ttk.Combobox(frame_add, values=["No", "Sí"], font=("arial", 10), state="readonly")
        combo_per.set("No")
        combo_per.place(x=10, y=180, width=260)

        tk.Label(frame_add, text="Vencimiento (AAAA-MM-DD):", font=("arial", 10)).place(x=10, y=210)
        ent_vence = tk.Entry(frame_add, font=("arial", 10), state="disabled", bg="#E0E0E0")
        ent_vence.insert(0, "No Aplica")
        ent_vence.place(x=10, y=230, width=260)

        # Alternar estado del campo de fecha según la opción perecedero
        def alternar_fecha(event):
            if combo_per.get() == "Sí":
                ent_vence.config(state="normal", bg="white")
                if ent_vence.get() == "No Aplica":
                    ent_vence.delete(0, tk.END)
            else:
                ent_vence.delete(0, tk.END)
                ent_vence.insert(0, "No Aplica")
                ent_vence.config(state="disabled", bg="#E0E0E0")

        combo_per.bind("<<ComboboxSelected>>", alternar_fecha)

        # Lógica del botón de guardado
        def ejecutar_guardado_articulo():
            n = ent_nom.get().strip()
            c_str = ent_cos.get().strip()
            p_str = ent_pre.get().strip()
            per_txt = combo_per.get()
            v_txt = ent_vence.get().strip()

            if not n or not c_str or not p_str:
                messagebox.showerror("Error", "Completa los datos del artículo.", parent=top_cat)
                return

            try:
                c = float(c_str)
                p = float(p_str)
            except ValueError:
                messagebox.showerror("Error", "Costo y precio deben ser valores numéricos.", parent=top_cat)
                return

            per_val = 1 if per_txt == "Sí" else 0
            v_val = None if (v_txt == "No Aplica" or v_txt == "") else v_txt

            if control_edicion["id_articulo"] is None:
                exito, msg = ctrl.agregar_producto_a_catalogo(id_prov, n, c, p, per_val, v_val)
            else:
                exito, msg = ctrl.actualizar_articulo_catalogo(control_edicion["id_articulo"], n, c, p, per_val, v_val)

            if exito:
                messagebox.showinfo("Éxito", msg, parent=top_cat)
                ent_nom.delete(0, tk.END)
                ent_cos.delete(0, tk.END)
                ent_pre.delete(0, tk.END)
                combo_per.set("No")
                alternar_fecha(None)

                if control_edicion["id_articulo"] is not None:
                    control_edicion["id_articulo"] = None
                    btn_guardar.config(text="Guardar en Catálogo", bg="#2196F3")

                refrescar_subtabla()

                # Hilo de refresco para el inventario de fondo
                def hilo_refresco_inventario():
                    try:
                        pantalla_inventario = None
                        for llave, instancia_frame in top_cat.controller.frames.items():
                            if "inventario" in instancia_frame.__class__.__name__.lower():
                                pantalla_inventario = instancia_frame
                                break
                        if pantalla_inventario and hasattr(pantalla_inventario, 'cargar_articulos'):
                            pantalla_inventario.cargar_articulos()
                    except Exception as e:
                        print(f"Aviso silencioso: {e}")

                top_cat.after(10, hilo_refresco_inventario)
            else:
                messagebox.showerror("Error", msg, parent=top_cat)

        def preparar_edicion(prod):
            id_p = prod[0] if len(prod) > 0 else None
            nom = prod[1] if len(prod) > 1 else ""
            cos = prod[2] if len(prod) > 2 else 0.0
            pre = prod[3] if len(prod) > 3 else 0.0
            stk = prod[4] if len(prod) > 4 else 0
            per = prod[5] if len(prod) > 5 else 0
            venc = prod[6] if len(prod) > 6 else None

            control_edicion["id_articulo"] = id_p
            
            ent_nom.delete(0, tk.END)
            ent_nom.insert(0, nom)
            ent_cos.delete(0, tk.END)
            ent_cos.insert(0, str(cos))
            ent_pre.delete(0, tk.END)
            ent_pre.insert(0, str(pre))
            
            combo_per.set("Sí" if per == 1 else "No")
            alternar_fecha(None)
            if per == 1 and venc:
                ent_vence.delete(0, tk.END)
                ent_vence.insert(0, str(venc))

            btn_guardar.config(text="Actualizar Artículo", bg="#FF9800")

        # Botón único con su color original
        btn_guardar = tk.Button(
            frame_add, text="Guardar en Catálogo", bg="#2196F3", fg="white",
            font=("arial", 10, "bold"), command=ejecutar_guardado_articulo
        )
        btn_guardar.place(x=10, y=280, width=260, height=35)

        refrescar_subtabla()

    def ver_historial_compras(self, id_proveedor):
        top_compras = tk.Toplevel(self)
        top_compras.title("Historial de Compras Realizadas")
        top_compras.geometry("700x450+400+150")
        top_compras.config(bg="#C6D9E3")
        top_compras.grab_set()

        frame_grid = tk.Frame(top_compras, bg="#C6D9E3")
        frame_grid.pack(padx=20, pady=20, fill="both", expand=True)

        headers = ["ID Compra", "Fecha de Transacción", "Monto Total Pagado", "Detalles / Notas"]
        for col_idx, text in enumerate(headers):
            tk.Label(frame_grid, text=text, font=("arial", 12, "bold"), bg="#9FB8C7", relief="groove", padx=5, pady=5).grid(row=0, column=col_idx, sticky="nsew")

        compras = ctrl.obtener_compras_proveedor(int(id_proveedor))
            
        if not compras:
            tk.Label(frame_grid, text="No se registran compras procesadas con este proveedor.", font=("arial", 12, "italic"), bg="#C6D9E3").grid(row=1, column=0, columnspan=4, pady=20)
            return

        for r_idx, comp in enumerate(compras, start=1):
            id_c, fecha, total, notas = comp
            c_fila = "#E1EBF0" if r_idx % 2 == 0 else "#F4F4F4"

            valores = [id_c, fecha, f"${total:,.2f}", notas]
            for c_idx, val in enumerate(valores):
                tk.Label(frame_grid, text=val, font=("arial", 11), bg=c_fila, relief="groove", anchor="w" if c_idx==3 else "center", padx=5, pady=4).grid(row=r_idx, column=c_idx, sticky="nsew")

        for i in range(4):
            frame_grid.grid_columnconfigure(i, weight=1 if i!=3 else 2)
            
    def ver_pedidos_pendientes(self, id_proveedor):
        top_pedidos = tk.Toplevel(self)
        top_pedidos.title("Órdenes y Pedidos Pendientes")
        top_pedidos.geometry("750x450+380+150")
        top_pedidos.config(bg="#C6D9E3")
        top_pedidos.grab_set()

        def refrescar_pedidos():
            for widget in frame_grid.winfo_children():
                widget.destroy()

            headers = ["ID", "Artículo / Producto", "Cantidad", "Costo Estimado", "Acción"]
            for col_idx, text in enumerate(headers):
                tk.Label(frame_grid, text=text, font=("arial", 12, "bold"), bg="#9FB8C7", relief="groove", padx=5, pady=5).grid(row=0, column=col_idx, sticky="nsew")

            pedidos = ctrl.obtener_pedidos_pendientes(id_proveedor)

            if not pedidos:
                tk.Label(frame_grid, text="No hay órdenes pendientes de entrega.", font=("arial", 12, "italic"), bg="#C6D9E3").grid(row=1, column=0, columnspan=5, pady=20)
                return

            for r_idx, ped in enumerate(pedidos, start=1):
                id_p, producto, cantidad, monto, estado = ped
                c_fila = "#E1EBF0" if r_idx % 2 == 0 else "#F4F4F4"

                valores = [id_p, producto, cantidad, f"${monto:,.2f}"]
                for c_idx, val in enumerate(valores):
                    tk.Label(frame_grid, text=val, font=("arial", 11), bg=c_fila, relief="groove", anchor="w" if c_idx==1 else "center", padx=5, pady=4).grid(row=r_idx, column=c_idx, sticky="nsew")

                btn_recibir = tk.Button(
                    frame_grid, text="Recibir", bg="#4CAF50", fg="white", font=("arial", 9, "bold"), bd=0, cursor="hand2",
                    command=lambda id_ped=id_p, prod=producto, cant=cantidad, mon=monto: abrir_recepcion(id_ped, prod, cant, mon)
                )
                btn_recibir.grid(row=r_idx, column=4, padx=5, pady=2)

            for i in range(5):
                frame_grid.grid_columnconfigure(i, weight=1 if i!=1 else 2)

        def abrir_recepcion(id_ped, producto, cantidad_esperada, monto_estimado):
            top_rec = tk.Toplevel(top_pedidos)
            top_rec.title(f"Recepción: {producto}")
            top_rec.geometry("400x500+400+100")
            top_rec.config(bg="#f4f4f4")
            top_rec.grab_set()

            costo_unitario = float(monto_estimado) / int(cantidad_esperada)
            precio_actual = ctrl.obtener_precio_actual_producto(producto)

            tk.Label(top_rec, text="Confirmación de Llegada", font=("arial", 14, "bold"), bg="#f4f4f4").pack(pady=10)

            info_frame = tk.Frame(top_rec, bg="#f4f4f4")
            info_frame.pack(fill="x", padx=20)
            tk.Label(info_frame, text=f"Producto: {producto}", font=("arial", 11), bg="#f4f4f4").pack(anchor="w")
            tk.Label(info_frame, text=f"Cantidad Esperada: {cantidad_esperada}", font=("arial", 11), bg="#f4f4f4").pack(anchor="w")
            tk.Label(info_frame, text=f"Costo Unitario Pago: ${costo_unitario:.2f}", font=("arial", 11, "bold"), fg="#D32F2F", bg="#f4f4f4").pack(anchor="w")

            tk.Label(top_rec, text="Cantidad Recibida Real:", font=("arial", 10, "bold"), bg="#f4f4f4").pack(anchor="w", padx=20, pady=(15,0))
            ent_cant = tk.Entry(top_rec, font=("arial", 12))
            ent_cant.insert(0, str(cantidad_esperada))
            ent_cant.pack(fill="x", padx=20)

            tk.Label(top_rec, text="Motivo del Faltante (Solo si llegó menos):", font=("arial", 10, "bold"), bg="#f4f4f4").pack(anchor="w", padx=20, pady=(15,0))
            ent_motivo = tk.Entry(top_rec, font=("arial", 12))
            ent_motivo.pack(fill="x", padx=20)

            tk.Label(top_rec, text="Fijar Precio de Venta Público ($):", font=("arial", 10, "bold"), bg="#f4f4f4").pack(anchor="w", padx=20, pady=(15,0))
            ent_precio = tk.Entry(top_rec, font=("arial", 12))
            if precio_actual > 0:
                ent_precio.insert(0, str(precio_actual))
            ent_precio.pack(fill="x", padx=20)

            def procesar():
                try:
                    cant_recibida = int(ent_cant.get())
                    nuevo_precio = float(ent_precio.get())
                except ValueError:
                    messagebox.showerror("Error", "Cantidad y precio deben ser numéricos.", parent=top_rec)
                    return

                motivo = ent_motivo.get().strip()
                if cant_recibida < cantidad_esperada and not motivo:
                    messagebox.showerror("Error", "Debe especificar un motivo si llegó menos cantidad.", parent=top_rec)
                    return

                exito, msj = ctrl.procesar_recepcion_pedido(id_ped, producto, cant_recibida, nuevo_precio, motivo)
                if exito:
                    messagebox.showinfo("Ingreso Confirmado", msj, parent=top_rec)
                    top_rec.destroy()
                    refrescar_pedidos()
                    for llave, inst in self.controller.frames.items():
                        if "inventario" in inst.__class__.__name__.lower() and hasattr(inst, 'cargar_articulos'):
                            inst.cargar_articulos()
                else:
                    messagebox.showerror("Error", msj, parent=top_rec)

            tk.Button(top_rec, text="✔ Ingresar al Inventario", bg="#4CAF50", fg="white", font=("arial", 12, "bold"), cursor="hand2", command=procesar).pack(pady=25)

        frame_grid = tk.Frame(top_pedidos, bg="#C6D9E3")
        frame_grid.pack(padx=20, pady=20, fill="both", expand=True)
        refrescar_pedidos()

    def seleccionar_proveedor(self, datos):
        self.id_proveedor_seleccionado = datos[0]
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, datos[1])
        
        self.entry_rif.delete(0, tk.END)
        self.entry_rif.insert(0, datos[2])
        
        self.entry_contacto.delete(0, tk.END)
        self.entry_contacto.insert(0, datos[3])

    def modificar_proveedor_ui(self):
        if not self.id_proveedor_seleccionado:
            messagebox.showwarning("Atención", "Haz clic sobre un proveedor en la tabla para seleccionarlo antes de actualizar.")
            return

        nom = self.entry_nombre.get().strip()
        rif = self.entry_rif.get().strip()
        tel = self.entry_contacto.get().strip()

        if not nom or not rif or not tel:
            messagebox.showerror("Error", "Todos los campos principales son obligatorios.")
            return

        exito, msj = ctrl.actualizar_proveedor(self.id_proveedor_seleccionado, nom, rif, tel)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.limpiar_formulario_proveedor()
            self.cargar_proveedores()
        else:
            messagebox.showerror("Error", msj)

    def eliminar_proveedor_ui(self):
        if not self.id_proveedor_seleccionado:
            messagebox.showwarning("Atención", "Haz clic sobre un proveedor en la tabla para seleccionarlo antes de eliminar.")
            return

        respuesta = messagebox.askyesno("Confirmar", "Al eliminar un proveedor se borrará también su historial de compras y catálogos.\n\n¿Estás seguro de eliminarlo permanentemente?")
        if respuesta:
            exito, msj = ctrl.eliminar_proveedor(self.id_proveedor_seleccionado)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.limpiar_formulario_proveedor()
                self.cargar_proveedores()
            else:
                messagebox.showerror("Error", msj)
    def limpiar_formulario_proveedor(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_rif.delete(0, tk.END)
        self.entry_contacto.delete(0, tk.END)
        
        if hasattr(self, 'id_proveedor_seleccionado'):
            self.id_proveedor_seleccionado = None