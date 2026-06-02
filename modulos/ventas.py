from tkinter import *
from tkinter import ttk,messagebox,simpledialog
import tkinter as tk
import especialidades.controlador as ctrl
import threading


class Ventas(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.numero_factura = self.obtener_num_factura()
        self.controller=controller
        self.widgets()
        self.producto_seleccionado = [] 
        self.precio_actual = 0.0
        self.stock_actual = 0
        self.total_venta_actual = 0.0

    def obtener_num_factura(self):
        return ctrl.obtener_num_factura()

    def inicializar_productos(self):
        lista_completa = ctrl.cargar_productos() 
        self.entry_producto['values'] = lista_completa

    def cargar_productos(self, event=None):
        if not self.entry_producto.get().strip():
            self.actualizar_datos_producto()
            return
        
        if hasattr(self, '_timer_producto_id') and self._timer_producto_id:
            self.after_cancel(self._timer_producto_id)
            
        self._timer_producto_id = self.after(1000, self.ejecutar_busqueda_producto_hilo)

    def ejecutar_busqueda_producto_hilo(self):
        texto_escrito = self.entry_producto.get()
        
        if texto_escrito == "":
            self.inicializar_productos()
            return
            
        def buscar_en_segundo_plano():
            lista_filtrada = ctrl.filtrar_nombre(texto_escrito)
            self.after(0, lambda: self.actualizar_interfaz_combo(lista_filtrada))
            
        hilo = threading.Thread(target=buscar_en_segundo_plano)
        hilo.daemon = True
        hilo.start()

    def actualizar_interfaz_combo(self, lista_filtrada):
        self.entry_producto['values'] = lista_filtrada
        
        if lista_filtrada:
            try:
                self.entry_producto.event_generate("<Down>")
            except tk.TclError:
                pass      
            self.entry_producto.icursor(tk.END) 
    
    def actualizar_datos_producto(self, event=None):
        producto_seleccionado = self.entry_producto.get()
        
        if producto_seleccionado:
            datos = ctrl.mostrar_vender(producto_seleccionado)
            
            if datos:
                self.precio_actual = datos[1]  # precio
                self.stock_actual = datos[2]   # stock
                
                self.label_stock.config(text=f"stock: {self.stock_actual}")
                self.label_precio_unitario.config(text=f"Precio unitario: ${self.precio_actual:.2f}")
            else:
                self.stock_actual = 0
                self.precio_actual = 0.0
                self.label_stock.config(text="stock: 0")
                self.label_precio_unitario.config(text="Precio unitario: $0.00")
        else:
            self.stock_actual = 0
            self.precio_actual = 0.0
            
            self.label_stock.config(text="stock: 0")
            self.label_precio_unitario.config(text="Precio unitario: $0.00")

    def actualizar_stock(self, event=None):
        producto_seleccionado=self.entry_producto.get()
        datos = ctrl.mostrar_vender(producto_seleccionado)
        if datos:
            self.stock_actual = datos[2]   
            self.label_stock.config(text=f"stock: {self.stock_actual}")

    def cargar_clientes(self, event=None):
        lista_nombres = ctrl.obtener_nombres_clientes()
        self.entry_cliente['values'] = lista_nombres

    def filtrar_clientes(self, event=None):
        if hasattr(self, '_timer_cliente_id') and self._timer_cliente_id:
            self.after_cancel(self._timer_cliente_id)
        
        self._timer_cliente_id = self.after(1000, self.ejecutar_busqueda_hilo)

    def ejecutar_busqueda_hilo(self):
        texto_escrito = self.entry_cliente.get()
        
        if texto_escrito == "":
            self.cargar_clientes()
            return

        def buscar_clientes_segundo_plano():
            lista_filtrada = ctrl.filtrar_clientes_por_nombre(texto_escrito)
            self.after(0, lambda: self.actualizar_interfaz_clientes(lista_filtrada))

        hilo = threading.Thread(target=buscar_clientes_segundo_plano)
        hilo.daemon = True
        hilo.start()

    def actualizar_interfaz_clientes(self, lista_filtrada):
        self.entry_cliente['values'] = lista_filtrada
        
        if lista_filtrada:
            try:
                self.entry_cliente.event_generate("<Down>") 
            except tk.TclError:
                pass
            self.entry_cliente.icursor(tk.END)

    def agregar_al_carrito(self):
        cliente = self.entry_cliente.get()
        producto = self.entry_producto.get()
        
        try:
            cantidad = int(self.entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese una cantidad válida.")
            return
            
        if not cliente:
            messagebox.showerror("Error", "Por favor, seleccione un cliente.")
            return
            
        if not producto:
            messagebox.showerror("Error", "Por favor, seleccione un producto.")
            return
            
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a cero.")
            return

        if cantidad > self.stock_actual:
            messagebox.showerror("Error", f"Cantidad excede el stock disponible ({self.stock_actual}).")
            return

        producto_ya_existe = False
        
        for item in self.tre.get_children():
            valores_fila = self.tre.item(item, 'values')
            
            if valores_fila[2] == producto:
                producto_ya_existe = True
                cantidad_anterior = int(valores_fila[4]) 
                nueva_cantidad_total = cantidad_anterior + cantidad
                
                nuevo_subtotal = self.precio_actual * nueva_cantidad_total
                subtotal_formateado = "{:.2f}".format(nuevo_subtotal)
                
                self.tre.item(item, values=(
                    valores_fila[0],      
                    valores_fila[1],    
                    producto,     
                    valores_fila[3],      
                    nueva_cantidad_total, 
                    subtotal_formateado   
                ))
                break

        if not producto_ya_existe:
            subtotal = self.precio_actual * cantidad
            subtotal_formateado = "{:.2f}".format(subtotal)
            self.tre.insert("", "end", values=(
                self.numero_factura, 
                cliente, 
                producto, 
                f"{self.precio_actual:.2f}", 
                cantidad, 
                subtotal_formateado
            ))

        self.entry_cliente.config(state="disabled")
        ctrl.reducir_stock(producto, cantidad)
        self.stock_actual -= cantidad
        self.label_stock.config(text=f"stock: {self.stock_actual}")
        self.actualizar_total_carrito()

    def actualizar_total_carrito(self):
        total_acumulado = 0.0

        for item in self.tre.get_children():
            valores = self.tre.item(item, 'values')
            try:
                subtotal_fila = float(valores[5])
                total_acumulado += subtotal_fila
            except (IndexError, ValueError):
                continue

        cliente_seleccionado = self.entry_cliente.get()
        
        porcentaje_iva = 0.16 
        
        if cliente_seleccionado:
            tipo_cliente = ctrl.tipo_cliente(cliente_seleccionado) 
            if tipo_cliente == "Jurídica":
                porcentaje_iva = 0.16  
            elif tipo_cliente == "Natural":
                porcentaje_iva = 0.16 

        monto_iva = total_acumulado * porcentaje_iva
        total_con_iva = total_acumulado + monto_iva

        self.total_venta_actual = total_con_iva

        self.lable_precio_total.config(text=f"Precio Total: ${total_con_iva:.2f}")

    def eliminar_articulo(self):
        seleccionado = self.tre.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un artículo para eliminar.")
            return
            
        if not messagebox.askyesno("Confirmar", "¿Desea eliminar este artículo del carrito?"):
            return
            
        for item in seleccionado:
            valores = self.tre.item(item, 'values')
            if not valores:
                continue
                
            producto = str(valores[2]).strip()
            cantidad = int(valores[4])
            
            ctrl.restaurar_stock(producto, cantidad)
            
            if self.entry_producto.get() == producto:
                self.stock_actual += cantidad
                self.label_stock.config(text=f"stock: {self.stock_actual}")
                
            self.tre.delete(item)
            
        if not self.tre.get_children():
            self.entry_cliente.config(state="normal")
            self.entry_cliente.set("")
            
        if hasattr(self.entry_producto, 'delete'):
            self.entry_producto.delete(0, tk.END)
        elif hasattr(self.entry_producto, 'set'):
            self.entry_producto.set("")
            
        self.actualizar_datos_producto()
            
        self.actualizar_total_carrito()
        messagebox.showinfo("Éxito", "Artículo removido correctamente.")

    def editar_carrito(self):
        selected_item = self.tre.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un artículo para editar.")
            return
            
        item_values = self.tre.item(selected_item[0], 'values')
        if not item_values:
            messagebox.showerror("Error", "Artículo seleccionado no válido.")
            return
            
        current_producto = item_values[2]
        current_cantidad = item_values[4]
        
        new_cantidad = simpledialog.askinteger(
            "Editar Cantidad", 
            f"Ingrese la nueva cantidad para {current_producto}: ", 
            initialvalue=int(current_cantidad)
        )
        if new_cantidad is None:
            return
            
        try:
            if new_cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a cero.")
                return
                
            diferencia = new_cantidad - int(current_cantidad)
            if diferencia == 0:
                return 
                
            if diferencia > 0:
                limite_maximo = self.stock_actual + int(current_cantidad)
                if new_cantidad > limite_maximo:
                    messagebox.showerror("Error", f"No hay suficiente stock. Máximo disponible: {limite_maximo}")
                    return
                    
            ctrl.reducir_stock(current_producto, diferencia)
            
            precio_unitario = float(item_values[3])
            nuevo_subtotal = precio_unitario * new_cantidad
            subtotal_formateado = "{:.2f}".format(nuevo_subtotal)
            
            self.tre.item(selected_item[0], values=(
                item_values[0],
                item_values[1],   
                current_producto,   
                item_values[3],      
                new_cantidad,      
                subtotal_formateado 
            ))
            
            if self.entry_producto.get() == current_producto:
                self.stock_actual -= diferencia
                self.label_stock.config(text=f"stock: {self.stock_actual}")
                
            self.actualizar_total_carrito()
            messagebox.showinfo("Éxito", "Cantidad actualizada correctamente.")
            
        except ValueError:
            messagebox.showerror("Error", "Error al procesar los datos numéricos de la fila.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un fallo inesperado: {e}")

    def cancelar_toda_la_venta(self):
        if hasattr(self, 'tre'):
            for item in self.tre.get_children():
                valores = self.tre.item(item, 'values')
                try:
                    producto = valores[2]
                    cantidad = int(valores[4])
                    ctrl.restaurar_stock(producto, cantidad)
                except IndexError:
                    continue
                    
            self.tre.delete(*self.tre.get_children())
            
        producto_pantalla = self.entry_producto.get()
        if producto_pantalla:
            self.stock_actual = ctrl.obtener_stock_actual(producto_pantalla)
            self.label_stock.config(text=f"stock: {self.stock_actual}")
            
        self.actualizar_total_carrito()
        self.entry_cliente.config(state="normal")
        self.entry_cliente.set("")
        
        # Limpieza del combobox de producto
        if hasattr(self.entry_producto, 'delete'):
            self.entry_producto.delete(0, tk.END)
        elif hasattr(self.entry_producto, 'set'):
            self.entry_producto.set("")
            
        self.actualizar_datos_producto()

    def realizar_pago(self):
        if self.total_venta_actual == 0.0:
            messagebox.showwarning("Advertencia", "No hay productos en el carrito para pagar.")
            return

        total_venta = self.total_venta_actual
        lista_productos_guardar = []
        
        for item in self.tre.get_children():
            valores = self.tre.item(item, 'values')
            producto = valores[2]
            precio = float(valores[3].replace(',', ''))
            cantidad = int(valores[4])
            subtotal = float(valores[5].replace(',', ''))
            
            lista_productos_guardar.append((producto, precio, cantidad, subtotal))

        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Realizar Pago")
        ventana_pago.geometry("400x400+450+80")
        ventana_pago.config(bg="#C6D9E3")
        ventana_pago.resizable(False, False)
        ventana_pago.transient(self.master)
        ventana_pago.grab_set()
        ventana_pago.focus_set()
        ventana_pago.lift()

        label_titulo = tk.Label(ventana_pago, text="Realizar Pago", font="arial 20 bold", bg="#C6D9E3")
        label_titulo.place(x=100, y=20)

        label_total = tk.Label(ventana_pago, text=f"Total a Pagar: ${total_venta:.2f}", font="arial 14 bold", bg="#C6D9E3")
        label_total.place(x=100, y=80)

        label_costo = tk.Label(ventana_pago, text="Ingrese el monto a pagar:", font="arial 14 bold", bg="#C6D9E3")
        label_costo.place(x=80, y=160)

        entry_costo = tk.Entry(ventana_pago, font="arial 14 bold")
        entry_costo.place(x=80, y=200, width=240, height=40)

        def confirmar_transaccion():
            try:
                monto_ingresado = float(entry_costo.get())
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese un monto numérico válido.", parent=ventana_pago)
                return

            if monto_ingresado < total_venta:
                messagebox.showerror("Error", f"El monto es insuficiente. Falta: ${total_venta - monto_ingresado:.2f}", parent=ventana_pago)
                return

            cambio = monto_ingresado - total_venta
            
            cliente_actual = self.entry_cliente.get()
            ctrl.guardar_venta_completa(self.numero_factura, cliente_actual, lista_productos_guardar, total_venta)

            messagebox.showinfo("Éxito", f"¡Pago procesado!\nCambio a entregar: ${cambio:.2f}", parent=ventana_pago)

            self.tre.delete(*self.tre.get_children())
            self.numero_factura = self.obtener_num_factura()
            self.label_numero_factura.config(text=f"{self.numero_factura}")
            self.total_venta_actual = 0.0
            self.lable_precio_total.config(text="Precio Total: $0.00")
            self.entry_cliente.config(state="normal")
            self.entry_cliente.set("") 
            
            ventana_pago.destroy()

        boton_confirmar = tk.Button(ventana_pago, text="Confirmar Pago", font="arial 14 bold", bg="#4CAF50", fg="white", command=confirmar_transaccion)
        boton_confirmar.place(x=100, y=280, width=200, height=40)
    
    def ver_ventas(self):
        self.modos_filtro = ["Mostrar Todo", "Diario", "Semanal", "Quincenal", "Mensual"]
        self.indice_filtro = 0

        toplabel = tk.Toplevel(self)
        toplabel.title("Ventas Realizadas")
        toplabel.geometry("950x600+450+80")
        toplabel.config(bg="#C6D9E3")
        toplabel.resizable(False, False)
        toplabel.transient(self.master)
        toplabel.grab_set()

        canvas_finanzas = tk.Frame(toplabel, bg="#C6D9E3")
        canvas_finanzas.place(x=20, y=80, width=910, height=500)

        self.bt1 = tk.Button(toplabel, text="Mostrar Todo", font="arial 12 bold", bg="#4CAF50", fg="white", command=self.rotar_y_filtrar)
        self.bt1.place(x=20, y=20, width=220, height=40)

        self.bt2 = tk.Button(toplabel, text="Descargar", font="arial 12 bold", bg="#2196F3", fg="white", command=self.descargar_pdf)
        self.bt2.place(x=260, y=20, width=220, height=40)

        self.canvas = tk.Canvas(canvas_finanzas, bg="#C6D9E3", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(canvas_finanzas, orient="vertical", command=self.canvas.yview)
        self.scrollbar_frame = tk.Frame(self.canvas, bg="#C6D9E3")

        self.scrollbar_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(self.canvas.find_withtag("all")[0], width=e.width)
        )

        self.canvas.create_window((0, 0), window=self.scrollbar_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.cargar_ventas()

    def cargar_ventas(self, datos=None):
        if not hasattr(self, 'scrollbar_frame') or not self.scrollbar_frame.winfo_exists():
            return

        for widget in self.scrollbar_frame.winfo_children():
            widget.destroy()

        headers = ["ID", "N° Factura", "Cliente", "Fecha", "Total General"]
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
            historial_ventas = datos
        else:
            historial_ventas = ctrl.obtener_ventas()

        for row_idx, venta in enumerate(historial_ventas, start=1):
            color_fila = "#E1EBF0" if row_idx % 2 == 0 else "#F4F8FA"

            for col_idx, valor in enumerate(venta):
                texto_celda = f"${valor:,.2f}" if col_idx == 4 else valor
                
                lbl_dato = tk.Label(
                    self.scrollbar_frame,
                    text=texto_celda,
                    font=("arial", 16),
                    bg=color_fila,
                    anchor="center" if col_idx in [0, 1, 3] else ("w" if col_idx == 2 else "e"),
                    padx=10,
                    pady=5
                )
                lbl_dato.grid(row=row_idx, column=col_idx, sticky="nsew")

        self.scrollbar_frame.grid_columnconfigure(0, weight=1)
        self.scrollbar_frame.grid_columnconfigure(1, weight=2)
        self.scrollbar_frame.grid_columnconfigure(2, weight=4)
        self.scrollbar_frame.grid_columnconfigure(3, weight=2)
        self.scrollbar_frame.grid_columnconfigure(4, weight=2)

    def rotar_y_filtrar(self):
        self.indice_filtro = (self.indice_filtro + 1) % len(self.modos_filtro)
        modo_actual = self.modos_filtro[self.indice_filtro]

        self.bt1.config(text=modo_actual)

        ventas_filtradas = ctrl.obtener_ventas_filtradas(modo_actual)

        self.cargar_ventas(datos=ventas_filtradas)

    def descargar_pdf(self):
        modo_reporte = self.bt1.cget("text")

        from tkinter import messagebox
        try:
            ctrl.exportar_ventas_pdf(modo_reporte)
            messagebox.showinfo("Éxito", f"¡Reporte PDF ({modo_reporte}) generado correctamente en Descargas!")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")

    def widgets(self):
        labelframe=tk.LabelFrame(self,font="arial 12 bold",bg="#C6D9E3") 
        labelframe.place(x=25,y=30,width=1150,height=200)

        label_cliente=tk.Label(labelframe,text="Cliente:",font="arial 14 bold",bg="#C6D9E3")
        label_cliente.place(x=10,y=10)
        self.entry_cliente=ttk.Combobox(labelframe,font="arial 14 bold")
        self.entry_cliente.bind("<<ComboboxSelected>>", self.cargar_clientes)
        self.entry_cliente.place(x=110, y=10, width=200, height=40)
        self.cargar_clientes()
        self.entry_cliente.bind("<KeyRelease>", self.filtrar_clientes)

        label_producto=tk.Label(labelframe,text="Producto:",font="arial 14 bold",bg="#C6D9E3")
        label_producto.place(x=10,y=60)
        self.entry_producto=ttk.Combobox(labelframe,font="arial 14 bold")
        self.entry_producto.bind("<<ComboboxSelected>>", self.actualizar_datos_producto)
        self.entry_producto.place(x=110,y=60,width=200,height=40)        
        self.inicializar_productos()
        self.entry_producto.bind("<KeyRelease>", self.cargar_productos)

        label_cantidad = tk.Label(labelframe, text="Cantidad:", font="arial 14 bold", bg="#C6D9E3")
        label_cantidad.place(x=400, y=10)
        
        self.entry_cantidad = tk.Spinbox(labelframe, from_=0, to=100, font="arial 14 bold", bg="white", bd=0)
        self.entry_cantidad.place(x=500, y=10, width=200, height=40)

        self.entry_cantidad.delete(0, "end")
        self.entry_cantidad.insert(0, "1")

        self.label_stock=tk.Label(labelframe,text="stock:",font="arial 14 bold",bg="#C6D9E3")
        self.label_stock.place(x=400,y=60)

        self.label_precio_unitario = tk.Label(self, text="Precio unitario: $0.00", font="arial 14 bold", bg="#C6D9E3")
        self.label_precio_unitario.place(x=775, y=40) 

        label_factura=tk.Label(labelframe,text="Numero de Factura:",font="arial 14 bold",bg="#C6D9E3")
        label_factura.place(x=750,y=60)

        self.label_numero_factura=tk.Label(labelframe,text=f"{self.numero_factura}",font="arial 14 bold",bg="#C6D9E3")
        self.label_numero_factura.place(x=950,y=60)

        boton_agregar=tk.Button(labelframe,text="Agregar al Carrito",font="arial 14 bold",bg="#4CAF50",fg="white",command=self.agregar_al_carrito)
        boton_agregar.place(x=100,y=135,width=200,height=40)

        boton_editar=tk.Button(labelframe,text="Editar",font="arial 14 bold",bg="#2196F3",fg="white",command=self.editar_carrito)
        boton_editar.place(x=350,y=135,width=200,height=40)

        boton_eliminar=tk.Button(labelframe,text="Eliminar del Carrito",font="arial 14 bold",bg="#F44336",fg="white",command=self.eliminar_articulo)
        boton_eliminar.place(x=600,y=135,width=200,height=40)

        boton_limpiar=tk.Button(labelframe,text="Limpiar",font="arial 14 bold",bg="#BA48D6",fg="white",command=self.cancelar_toda_la_venta)
        boton_limpiar.place(x=850,y=135,width=200,height=40)

        treFrame=tk.Frame(self,bg="white")
        treFrame.place(x=25,y=250,width=1150,height=300)

        scrol_y=tk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT,fill=Y)

        self.tre=ttk.Treeview(treFrame,columns=("Factura","Cliente","Producto","Precio","Cantidad","Total"),yscrollcommand=scrol_y.set, height=40,show="headings")
        self.tre.pack(fill=BOTH,expand=True)
        self.tre.heading("Factura",text="Factura")
        self.tre.heading("Cliente",text="Cliente")
        self.tre.heading("Producto",text="Producto")
        self.tre.heading("Precio",text="Precio")
        self.tre.heading("Cantidad",text="Cantidad")
        self.tre.heading("Total",text="Total")

        scrol_y.config(command=self.tre.yview)

        self.tre.column("Factura",width=70,anchor=CENTER)
        self.tre.column("Cliente",width=150,anchor=CENTER)
        self.tre.column("Producto",width=150,anchor=CENTER)
        self.tre.column("Precio",width=100,anchor=CENTER)
        self.tre.column("Cantidad",width=100,anchor=CENTER)
        self.tre.column("Total",width=100,anchor=CENTER)

        self.lable_precio_total = tk.Label(self, text="Precio Total: $0.00", font="arial 14 bold", bg="#C6D9E3")
        self.lable_precio_total.place(x=900, y=575)
    
        boton_pagar=tk.Button(self,text="Pagar",font="arial 14 bold",bg="#4CAF50",fg="white",command=self.realizar_pago)
        boton_pagar.place(x=70,y=575,width=220,height=40)

        boton_ver_ventas=tk.Button(self,text="Ver Ventas Realizadas",font="arial 14 bold",bg="#2196F3",fg="white",command=self.ver_ventas)
        boton_ver_ventas.place(x=350,y=575,width=220,height=40)

   