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
        """labelframe=LabelFrame(self,text="Pedidos",font="arial 20 bold",bg="#C6D9E3")
        labelframe.place(x=20,y=20,width=400,height=200)

        lavel_proveedor=Label(labelframe,text="Proveedor:",font="arial 14 bold",bg="#C6D9E3")
        lavel_proveedor.place(x=10,y=10)
        self.entry_proveedor=ttk.Combobox(labelframe,font="arial 14 bold")
        self.entry_proveedor.bind("<<ComboboxSelected>>", self.cargar_proveedores)
        self.entry_proveedor.place(x=110,y=10,width=200,height=40)
        self.cargar_proveedores()
        self.entry_proveedor.bind("<<KeyRelease>>", self.filtrar_proveedores)

    def procesar_y_exportar_pedido(self):
        productos_pedidos = []
        
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
                
        if not productos_pedidos:
            messagebox.showwarning("Pedido Vacío", "No has ingresado cantidades válidas para ningún producto.")
            return

        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")],
            title="Exportar Orden de Pedido"
        )
        
        if not ruta_archivo:
            return

        try:
            with open(ruta_archivo, mode="w", newline="", encoding="utf-8-sig") as f:
                escritor = csv.writer(f, delimiter=";")
                escritor.writerow(["Producto / Artículo", "Cantidad Solicitada", "Costo Unitario", "Total Fila"])
                
                total_general = 0
                for item in productos_pedidos:
                    total_fila = item["cantidad"] * float(item["costo"])
                    total_general += total_fila
                    escritor.writerow([item["nombre"], item["cantidad"], f"${item['costo']}", f"${total_fila:.2f}"])
                    
                escritor.writerow([])
                escritor.writerow(["", "", "TOTAL DE LA ORDEN:", f"${total_general:.2f}"])
                
            messagebox.showinfo("Éxito", f"Pedido exportado correctamente a:\n{ruta_archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

    def exportar_a_csv(self, lista_productos):
        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")],
            title="Guardar Orden de Pedido"
        )
        
        if not ruta_guardado:
            return 

        try:
            with open(ruta_guardado, mode="w", newline="", encoding="utf-8-sig") as archivo:
                escritor = csv.writer(archivo, delimiter=";") 
                
                escritor.writerow(["Descripción del Artículo", "Cantidad Pedida", "Costo Unitario", "Total"])
                
                for item in lista_productos:
                    total_articulo = int(item["cantidad"]) * float(item["costo"])
                    escritor.writerow([
                        item["nombre"], 
                        item["cantidad"], 
                        item["costo"], 
                        total_articulo
                    ])
                    
            messagebox.showinfo("Éxito", f"Pedido descargado correctamente en:\n{ruta_guardado}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el CSV: {e}")

    def cargar_catalogo_pedido(self, event=None):
    
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