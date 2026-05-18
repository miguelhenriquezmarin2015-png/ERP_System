from tkinter import *
from tkinter import ttk,messagebox,simpledialog
import tkinter as tk
import modulos.controlador as ctrl


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
    
    def cargar_productos(self):
        return ctrl.cargar_productos()
    
    def actualizar_datos_producto(self, event=None):
        producto_seleccionado = self.entry_producto.get()
        
        if producto_seleccionado:
            datos = ctrl.mostrar_vender(producto_seleccionado)
            
            if datos:
                self.precio_actual = datos[1]  # precio
                self.stock_actual = datos[2]   # stock
                
                # CORRECCIÓN: Actualizamos las dos etiquetas de la interfaz
                self.label_stock.config(text=f"stock: {self.stock_actual}")
                self.label_precio_unitario.config(text=f"Precio unitario: ${self.precio_actual:.2f}")
            else:
                self.stock_actual = 0
                self.precio_actual = 0.0
            
    def actualizar_stock(self, event=None):
        producto_seleccionado=self.entry_producto.get()
        datos = ctrl.mostrar_vender(producto_seleccionado)
        if datos:
            self.stock_actual = datos[2]   # stock
            self.label_stock.config(text=f"stock: {self.stock_actual}")

    def cargar_clientes(self, event=None):
        lista_nombres = ctrl.obtener_nombres_clientes()
        self.entry_cliente['values'] = lista_nombres


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

        if cantidad > self.stock_actual:
            messagebox.showerror("Error", f"Cantidad excede el stock disponible ({self.stock_actual}).")
            return

        subtotal = self.precio_actual * cantidad
        subtotal_formateado = "{:,.1f}".format(subtotal)

        self.tre.insert("", "end", values=(self.numero_factura, cliente, producto, f"{self.precio_actual:.2f}", cantidad, f"{subtotal_formateado}"))
        
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
                
        self.total_venta_actual = total_acumulado
        self.lable_precio_total.config(text=f"Precio Total: ${total_acumulado:.2f}")

    def eliminar_articulo_carrito(self):
        seleccionado = self.tre.selection()
        if not seleccionado:
            return
            
        for item in seleccionado:
            valores = self.tre.item(item, 'values')
            producto = valores[2] 
            cantidad = int(valores[4])
            
            ctrl.restaurar_stock(producto, cantidad)
            
            if self.entry_producto.get() == producto:
                self.stock_actual += cantidad
                self.label_stock.config(text=f"stock: {self.stock_actual}")
                
            self.tre.delete(item)
            
        self.actualizar_total_carrito()

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
            self.actualizar_total_carrito()


    def realizar_pago(self):
        if self.total_venta_actual == 0.0:
            messagebox.showwarning("Advertencia", "No hay productos en el carrito para pagar.")
            return

        total_venta = 0.0
        lista_productos_guardar = []
        
        for item in self.tre.get_children():
            valores = self.tre.item(item, 'values')
            producto = valores[2]
            precio = float(valores[3].replace(',', ''))
            cantidad = int(valores[4])
            subtotal = float(valores[5].replace(',', ''))
            
            total_venta += subtotal
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
            
            ventana_pago.destroy()

        boton_confirmar = tk.Button(ventana_pago, text="Confirmar Pago", font="arial 14 bold", bg="#4CAF50", fg="white", command=confirmar_transaccion)
        boton_confirmar.place(x=100, y=280, width=200, height=40)

    def widgets(self):
        labelframe=tk.LabelFrame(self,font="arial 12 bold",bg="#C6D9E3") 
        labelframe.place(x=25,y=30,width=1150,height=200)

        label_cliente=tk.Label(labelframe,text="Cliente:",font="arial 14 bold",bg="#C6D9E3")
        label_cliente.place(x=10,y=10)
        self.entry_cliente=ttk.Combobox(labelframe,font="arial 14 bold")
        self.entry_cliente.bind("<<ComboboxSelected>>", self.cargar_clientes)
        self.entry_cliente.place(x=110,y=10,width=200,height=40)
        self.cargar_clientes()

        label_producto=tk.Label(labelframe,text="Producto:",font="arial 14 bold",bg="#C6D9E3")
        label_producto.place(x=10,y=60)
        self.entry_producto=ttk.Combobox(labelframe,font="arial 14 bold")
        # Busca la línea donde declaras tu Combobox de productos y añade esto abajo:
        self.entry_producto.bind("<<ComboboxSelected>>", self.actualizar_datos_producto)
        self.entry_producto.place(x=110,y=60,width=200,height=40)
        self.entry_producto['values'] = self.cargar_productos()

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

        boton_editar=tk.Button(labelframe,text="Editar",font="arial 14 bold",bg="#2196F3",fg="white")
        boton_editar.place(x=350,y=135,width=200,height=40)

        boton_eliminar=tk.Button(labelframe,text="Eliminar del Carrito",font="arial 14 bold",bg="#F44336",fg="white",command=self.eliminar_articulo_carrito)
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
        self.lable_precio_total.place(x=600, y=575)
    
        boton_pagar=tk.Button(self,text="Pagar",font="arial 14 bold",bg="#4CAF50",fg="white",command=self.realizar_pago)
        boton_pagar.place(x=70,y=575,width=220,height=40)

        boton_ver_ventas=tk.Button(self,text="Ver Ventas Realizadas",font="arial 14 bold",bg="#2196F3",fg="white")
        boton_ver_ventas.place(x=350,y=575,width=220,height=40)