from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
import especialidades.controlador as ctrl
import threading

class Proveedor(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
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

        self.boton_guardar = tk.Button(labelproveedor, text="Guardar", font="arial 14 bold", bg="#4CAF50", fg="white",command=self.guardar_nuevo_proveedor)
        self.boton_guardar.place(x=10, y=410, width=230, height=40)

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
        try:
            id_prov = datos_proveedor[0]
            nombre_prov = datos_proveedor[1]
        except (TypeError, IndexError):
            id_prov = datos_proveedor
            nombre_prov = "Proveedor"

        control_edicion = {"id_articulo": None}

        top_cat = tk.Toplevel(self)
        top_cat.title(f"Catálogo Autónomo - {nombre_prov}")
        top_cat.geometry("900x500+320+120")
        top_cat.config(bg="#C6D9E3")
        top_cat.grab_set()

        frame_add = tk.LabelFrame(top_cat, text="Añadir Artículo al Negocio", font="arial 11 bold", bg="#C6D9E3")
        frame_add.place(x=10, y=10, width=260, height=480)

        tk.Label(frame_add, text="Nombre Producto:", font="arial 10 bold", bg="#C6D9E3").place(x=10, y=10)
        ent_nom = tk.Entry(frame_add, font="arial 11")
        ent_nom.place(x=10, y=35, width=230, height=28)

        tk.Label(frame_add, text="Costo Prov ($):", font="arial 10 bold", bg="#C6D9E3").place(x=10, y=80)
        ent_cos = tk.Entry(frame_add, font="arial 11")
        ent_cos.place(x=10, y=105, width=230, height=28)

        tk.Label(frame_add, text="Precio Venta ($):", font="arial 10 bold", bg="#C6D9E3").place(x=10, y=150)
        ent_pre = tk.Entry(frame_add, font="arial 11")
        ent_pre.place(x=10, y=175, width=230, height=28)

        frame_tabla_base = tk.Frame(top_cat, bg="#C6D9E3")
        frame_tabla_base.place(x=280, y=15, width=600, height=470)

        canvas_sub = tk.Canvas(frame_tabla_base, bg="#C6D9E3", highlightthickness=0)
        scroll_sub = tk.Scrollbar(frame_tabla_base, orient="vertical", command=canvas_sub.yview)
        frame_grid_sub = tk.Frame(canvas_sub, bg="#C6D9E3")

        frame_grid_sub.bind("<Configure>", lambda e: canvas_sub.configure(scrollregion=canvas_sub.bbox("all")))
        canvas_sub.create_window((0, 0), window=frame_grid_sub, anchor="nw", width=565)
        canvas_sub.configure(yscrollcommand=scroll_sub.set)
        canvas_sub.place(x=0, y=0, width=565, height=470)
        scroll_sub.place(x=565, y=0, width=25, height=470)

        def refrescar_subtabla():
            for w in frame_grid_sub.winfo_children():
                w.destroy()

            headers_cat = ["ID", "Producto / Artículo", "Costo", "P. Venta", "Stock", "Acción"]
            for c_idx, text in enumerate(headers_cat):
                tk.Label(
                    frame_grid_sub, text=text, font=("arial", 12, "bold"), 
                    bg="#9FB8C7", relief="groove", padx=5, pady=5
                ).grid(row=0, column=c_idx, sticky="nsew")

            productos = ctrl.obtener_catalogo_por_proveedor(id_prov)
            for r_idx, prod in enumerate(productos, start=1):
                id_p, n_p, c_p, p_p, s_p = prod
                c_fila = "#E1EBF0" if r_idx % 2 == 0 else "#F4F4F4"

                valores_p = [id_p, n_p, f"${c_p:.2f}", f"${p_p:.2f}", s_p]
                for c_idx, val in enumerate(valores_p):
                    anchor_val = "w" if c_idx == 1 else "center"
                    tk.Label(
                        frame_grid_sub, text=val, font=("arial", 11), bg=c_fila, 
                        relief="groove", anchor=anchor_val
                    ).grid(row=r_idx, column=c_idx, sticky="nsew")

                def preparar_edicion(ip=id_p, nom=n_p, cos=c_p, pre=p_p):
                    control_edicion["id_articulo"] = ip
                    ent_nom.delete(0, tk.END)
                    ent_nom.insert(0, nom)
                    ent_cos.delete(0, tk.END)
                    ent_cos.insert(0, str(cos))
                    ent_pre.delete(0, tk.END)
                    ent_pre.insert(0, str(pre))
                    btn_guardar.config(text="Actualizar Artículo", bg="#FF9800")

                btn_edit = tk.Button(
                    frame_grid_sub, text="Modificar", bg=c_fila, font=("arial", 10),
                    bd=1, relief="groove", cursor="hand2", command=preparar_edicion
                )
                btn_edit.grid(row=r_idx, column=5, sticky="nsew", padx=2, pady=1)

            # Configurar anchos de columna (ahora son 6 columnas: de la 0 a la 5)
            for i in range(6):
                frame_grid_sub.grid_columnconfigure(i, weight=1 if i != 1 else 2)

        def ejecutar_guardado_articulo():
            n = ent_nom.get().strip()
            c_str = ent_cos.get().strip()
            p_str = ent_pre.get().strip()

            if not n or not c_str or not p_str:
                messagebox.showerror("Error", "Completa los datos del artículo.", parent=top_cat)
                return

            try:
                c = float(c_str)
                p = float(p_str)
            except ValueError:
                messagebox.showerror("Error", "Costo y precio deben ser valores numéricos.", parent=top_cat)
                return

            if control_edicion["id_articulo"] is None:
                exito, msg = ctrl.agregar_producto_a_catalogo(id_prov, n, c, p)
            else:
                exito, msg = ctrl.actualizar_articulo_catalogo(control_edicion["id_articulo"], n, c, p)

            if exito:
                messagebox.showinfo("Éxito", msg, parent=top_cat)
                ent_nom.delete(0, tk.END)
                ent_cos.delete(0, tk.END)
                ent_pre.delete(0, tk.END)
                
                if control_edicion["id_articulo"] is not None:
                    control_edicion["id_articulo"] = None
                    btn_guardar.config(text="Guardar en Catálogo", bg="#2196F3")
                    
                refrescar_subtabla()
            else:
                messagebox.showerror("Error", msg, parent=top_cat)

        btn_guardar = tk.Button(
            frame_add, text="Guardar en Catálogo", bg="#2196F3", fg="white", 
            font="arial 10 bold", command=ejecutar_guardado_articulo
        )
        btn_guardar.place(x=10, y=220, width=230, height=35)

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

            pedidos = ctrl.obtener_pedidos_pendientes(int(id_proveedor))
            
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
                    frame_grid, text="Recibido", bg="#4CAF50", fg="white", font=("arial", 9, "bold"), bd=0,
                    command=lambda id_ped=id_p: marcar_como_recibido(id_ped)
                )
                btn_recibir.grid(row=r_idx, column=4, padx=5, pady=2)

            for i in range(5):
                frame_grid.grid_columnconfigure(i, weight=1 if i!=1 else 2)

        def marcar_como_recibido(id_ped):
            if ctrl.recibir_pedido_pendiente_db(id_ped):
                messagebox.showinfo("Éxito", "¡El pedido ha sido marcado como recibido correctamente!", parent=top_pedidos)
                refrescar_pedidos() 
                pantalla_inventario = None
                for llave, instancia_frame in self.controller.frames.items():
                    # Con __class__.__name__ obtenemos el nombre de la clase como texto (ej. "Inventario")
                    if "inventario" in instancia_frame.__class__.__name__.lower():
                        pantalla_inventario = instancia_frame
                        break
                
                # Si la encuentra y tiene el método, fuerza la recarga de los artículos
                if pantalla_inventario and hasattr(pantalla_inventario, 'cargar_articulos'):
                    pantalla_inventario.cargar_articulos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el estado del pedido.", parent=top_pedidos)

        frame_grid = tk.Frame(top_pedidos, bg="#C6D9E3")
        frame_grid.pack(padx=20, pady=20, fill="both", expand=True)
        
        refrescar_pedidos()
