from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import especialidades.controlador as ctrl

class Finanzas(tk.Frame):
    def __init__(self, padre, controller):
        super().__init__(padre)
        self.controller = controller
        self.tipo_filtro = "Todo"  
        self.widgets()

    def widgets(self):
        # ================= PANEL IZQUIERDO (OPCIONES Y FILTROS) =================
        lblframa_botones = LabelFrame(self, text="Opciones Financieras", font="arial 12 bold", bg="#C6D9E3")
        lblframa_botones.place(x=20, y=20, width=250, height=625)

        tk.Button(lblframa_botones, text="Fondos y Ahorros", font="arial 11 bold", bg="#FFC107", fg="black", cursor="hand2", command=self.abrir_fondos).place(x=10, y=20, width=220, height=45)
        tk.Button(lblframa_botones, text="Registrar Gasto", font="arial 11 bold", bg="#F44336", fg="white", cursor="hand2", command=self.registrar_gasto).place(x=10, y=80, width=220, height=45)
        
        tk.Button(lblframa_botones, text="Añadir Capital", font="arial 11 bold", bg="#8BC34A", fg="white", cursor="hand2", command=self.registrar_inversion_ui).place(x=10, y=140, width=220, height=45)

        tk.Label(lblframa_botones, text="Filtros de Movimientos:", bg="#C6D9E3", font="arial 10 bold").place(x=10, y=195)
        tk.Button(lblframa_botones, text="Ver Todo", font="arial 11 bold", bg="#90CAF9", cursor="hand2", command=lambda: self.filtrar_movimientos("Todo")).place(x=10, y=220, width=220, height=35)
        tk.Button(lblframa_botones, text="Mostrar Ingresos", font="arial 11 bold", bg="#A5D6A7", cursor="hand2", command=lambda: self.filtrar_movimientos("Ingresos")).place(x=10, y=265, width=220, height=35)
        tk.Button(lblframa_botones, text="Mostrar Egresos", font="arial 11 bold", bg="#EF9A9A", cursor="hand2", command=lambda: self.filtrar_movimientos("Egresos")).place(x=10, y=310, width=220, height=35)

        # ================= PANEL DERECHO (DASHBOARD GENERAL) =================
        self.lbl_balance = tk.Label(self, text="Balance General: $0.00", font=("arial", 20, "bold"), bg="#4CAF50", fg="white", relief="ridge")
        self.lbl_balance.place(x=290, y=20, width=900, height=60)

        canvas_fondo = tk.Label(self, bg="#C6D9E3")
        canvas_fondo.place(x=290, y=90, width=900, height=555)

        self.canvas = tk.Canvas(canvas_fondo, bg="#FFFFFF")
        self.scrollbar = Scrollbar(canvas_fondo, orient="vertical", command=self.canvas.yview)
        self.scrollbar_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        
        self.scrollbar_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0,0), window=self.scrollbar_frame, anchor="nw", width=880)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.actualizar_pantalla()

    def actualizar_pantalla(self):
        datos_balance = ctrl.calcular_balance_general()
        bal = datos_balance["balance_disponible"]
        color_bg = "#4CAF50" if bal >= 0 else "#D32F2F"
        self.lbl_balance.config(text=f"Balance General Disponible: ${bal:,.2f}", bg=color_bg)
        self.cargar_movimientos()

    def filtrar_movimientos(self, tipo):
        self.tipo_filtro = tipo
        self.cargar_movimientos()

    def cargar_movimientos(self):
        for widget in self.scrollbar_frame.winfo_children():
            widget.destroy()

        headers = ["Tipo", "Descripción / Concepto", "Fecha y Hora", "Monto"]
        for col_idx, text in enumerate(headers):
            tk.Label(self.scrollbar_frame, text=text, font=("arial", 12, "bold"), bg="#9FB8C7", fg="black", relief="groove", padx=5, pady=5).grid(row=0, column=col_idx, sticky="nsew")

        movimientos = ctrl.obtener_movimientos(self.tipo_filtro)

        if not movimientos:
            tk.Label(self.scrollbar_frame, text="No hay movimientos para mostrar.", font=("arial", 12, "italic"), bg="#FFFFFF").grid(row=1, column=0, columnspan=4, pady=20)
            return

        for row_idx, mov in enumerate(movimientos, start=1):
            color_fila = "#F0F4F8" if row_idx % 2 == 0 else "#FFFFFF"
            id_m, tipo, desc, fecha, monto = mov
            
            color_texto = "#388E3C" if ("Ingreso" in tipo or "inversión" in tipo) else "#D32F2F"

            valores = [tipo, desc, fecha, f"${float(monto):,.2f}"]
            for col_idx, valor in enumerate(valores):
                tk.Label(
                    self.scrollbar_frame, text=valor, font=("arial", 11), bg=color_fila, 
                    fg=color_texto if col_idx == 3 or col_idx == 0 else "black",
                    anchor="center" if col_idx in [0, 2] else ("w" if col_idx == 1 else "e"), padx=10, pady=6
                ).grid(row=row_idx, column=col_idx, sticky="nsew")

        self.scrollbar_frame.grid_columnconfigure(0, weight=1) 
        self.scrollbar_frame.grid_columnconfigure(1, weight=3) 
        self.scrollbar_frame.grid_columnconfigure(2, weight=2) 
        self.scrollbar_frame.grid_columnconfigure(3, weight=1)

    def registrar_gasto(self):
        top = tk.Toplevel(self)
        top.title("Registrar Nuevo Gasto / Egreso")
        top.geometry("400x320+450+200")
        top.config(bg="#f4f4f4")
        top.grab_set()

        tk.Label(top, text="Descripción del Gasto:", font=("arial", 11, "bold"), bg="#f4f4f4").pack(pady=(15, 5))
        ent_desc = tk.Entry(top, font=("arial", 12), width=30)
        ent_desc.pack()

        tk.Label(top, text="Monto ($):", font=("arial", 11, "bold"), bg="#f4f4f4").pack(pady=(15, 5))
        ent_monto = tk.Entry(top, font=("arial", 12), width=30)
        ent_monto.pack()

        tk.Label(top, text="¿Debitar de algún fondo? (Opcional):", font=("arial", 11, "bold"), bg="#f4f4f4").pack(pady=(15, 5))
        
        fondos = ctrl.obtener_lista_fondos()
        valores_combo = ["No (Debitar del Balance General)"] + [f"{f[0]} - {f[1]} (Saldo: ${f[2]:.2f})" for f in fondos]
        
        combo_fondos = ttk.Combobox(top, values=valores_combo, state="readonly", width=38, font=("arial", 10))
        combo_fondos.current(0)
        combo_fondos.pack()

        def procesar_gasto():
            desc = ent_desc.get().strip()
            try:
                monto = float(ent_monto.get())
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número válido.", parent=top)
                return
            
            if not desc or monto <= 0:
                messagebox.showerror("Error", "Complete todos los campos correctamente.", parent=top)
                return

            seleccion = combo_fondos.get()
            id_fondo = None
            if seleccion != "No (Debitar del Balance General)":
                id_fondo = int(seleccion.split("-")[0].strip())

            exito, msj = ctrl.registrar_egreso(desc, monto, id_fondo)
            if exito:
                messagebox.showinfo("Éxito", msj, parent=top)
                top.destroy()
                self.actualizar_pantalla()
            else:
                messagebox.showerror("Fondos Insuficientes", msj, parent=top)

        tk.Button(top, text="Guardar Gasto", font=("arial", 11, "bold"), bg="#F44336", fg="white", cursor="hand2", command=procesar_gasto).pack(pady=20)

    def abrir_fondos(self):
        top = tk.Toplevel(self)
        top.title("Gestión de Fondos y Ahorros")
        top.geometry("500x350+400+180")
        top.config(bg="#C6D9E3")
        top.grab_set()

        tk.Label(top, text="Tus Fondos de Ahorro", font=("arial", 16, "bold"), bg="#C6D9E3").pack(pady=10)

        frame_fondos = tk.Frame(top, bg="#FFFFFF", bd=2, relief="groove")
        frame_fondos.pack(fill="both", expand=True, padx=20, pady=10)

        def refrescar_lista_fondos():
            for widget in frame_fondos.winfo_children():
                widget.destroy()
            
            fondos = ctrl.obtener_lista_fondos()
            for f in fondos:
                id_f, nombre, saldo = f
                row_frame = tk.Frame(frame_fondos, bg="#FFFFFF")
                row_frame.pack(fill="x", padx=10, pady=8)
                
                tk.Label(row_frame, text=nombre, font=("arial", 11, "bold"), bg="#FFFFFF", anchor="w", width=25).pack(side="left")
                tk.Label(row_frame, text=f"${float(saldo):,.2f}", font=("arial", 11), bg="#FFFFFF", fg="#388E3C").pack(side="left")
                
                tk.Button(
                    row_frame, text="+ Añadir", bg="#2196F3", fg="white", font=("arial", 9, "bold"), cursor="hand2",
                    command=lambda i=id_f, n=nombre: ingresar_dinero_fondo(i, n)
                ).pack(side="right")

        def ingresar_dinero_fondo(id_fondo, nombre_fondo):
            monto = simpledialog.askfloat("Ingresar Dinero", f"¿Cuánto deseas transferir al '{nombre_fondo}'?\n(Este dinero se descontará de tu Balance General)", parent=top, minvalue=0.01)
            if monto:
                exito, msj = ctrl.transferir_a_fondo(id_fondo, monto)
                if exito:
                    messagebox.showinfo("Éxito", msj, parent=top)
                    refrescar_lista_fondos()
                    self.actualizar_pantalla()
                else:
                    messagebox.showerror("Error", msj, parent=top)

        refrescar_lista_fondos()

    def registrar_inversion_ui(self):
            top = tk.Toplevel(self)
            top.title("Registrar Capital / Inversión")
            top.geometry("400x250+450+200")
            top.config(bg="#f4f4f4")
            top.grab_set()

            tk.Label(top, text="Origen del Capital (Ej: Inversionista, Préstamo):", font=("arial", 10, "bold"), bg="#f4f4f4").pack(pady=(15, 5))
            ent_desc = tk.Entry(top, font=("arial", 12), width=30)
            ent_desc.pack()

            tk.Label(top, text="Monto a Invertir ($):", font=("arial", 10, "bold"), bg="#f4f4f4").pack(pady=(15, 5))
            ent_monto = tk.Entry(top, font=("arial", 12), width=30)
            ent_monto.pack()

            def procesar_capital():
                desc = ent_desc.get().strip()
                try:
                    monto = float(ent_monto.get())
                except ValueError:
                    messagebox.showerror("Error", "El monto debe ser un número válido.", parent=top)
                    return
                
                if not desc or monto <= 0:
                    messagebox.showerror("Error", "Complete los campos. El monto debe ser mayor a cero.", parent=top)
                    return

                exito, msj = ctrl.registrar_inversion(desc, monto)
                if exito:
                    messagebox.showinfo("Éxito", msj, parent=top)
                    top.destroy()
                    self.actualizar_pantalla()
                else:
                    messagebox.showerror("Error", msj, parent=top)

            tk.Button(top, text="Ingresar Capital al Sistema", font=("arial", 11, "bold"), bg="#4CAF50", fg="white", cursor="hand2", command=procesar_capital).pack(pady=20)