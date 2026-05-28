from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
import especialidades.controlador as ctrl

class Finanzas(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()
        self.modos_filtro = ["Mostrar Todo", "Diario", "Semanal", "Quincenal", "Mensual"]
        self.indice_filtro = 0  

    def widgets(self):
        canvas_finanzas=tk.Label(self,text="Ventas Realizadas ",font="arial 20 bold",bg="#C6D9E3")
        canvas_finanzas.place(x=300,y=20,width=890,height=625)

        self.canvas=tk.Canvas(canvas_finanzas)
        self.scrollbar=Scrollbar(canvas_finanzas,orient="vertical",command=self.canvas.yview)
        self.scrollbar_frame=tk.Frame(self.canvas,bg="#C6D9E3")
        self.scrollbar_frame.bind(
            "<Configure>"
            ,lambda e: self.canvas.configure
            (scrollregion=self.canvas.bbox("all")
             )
        )
        self.canvas.bind("<Configure>"
                         ,lambda e: self.canvas.itemconfig(self.canvas.find_withtag("all")[0],width=e.width))
        self.canvas.create_window((0,0),window=self.scrollbar_frame,anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left",fill="both",expand=True)
        self.scrollbar.pack(side="right",fill="y")

#obsiones

        lblframa_botones=LabelFrame(self,text="Opciones",font="arial 12 bold",bg="#C6D9E3")
        lblframa_botones.place(x=20,y=20,width=250,height=540)

        self.bt1=tk.Button(lblframa_botones,text="Mostrar todo",font="arial 12 bold",bg="#4CAF50",fg="white",command=self.rotar_y_filtrar)
        self.bt1.place(x=10,y=10,width=220,height=40)

        self.bt2=tk.Button(lblframa_botones,text="Descargar",font="arial 12 bold",bg="#2196F3",fg="white",command=self.descargar_pdf)
        self.bt2.place(x=10,y=60,width=220,height=40)

        self.cargar_ventas()

    def cargar_ventas(self, datos=None):
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
                if col_idx == 4:
                    texto_celda = f"${valor:,.2f}"
                else:
                    texto_celda = valor

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
                
                lbl_dato.bind("<Button-1>", lambda event, v=venta: self.seleccionar_factura(v))

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

