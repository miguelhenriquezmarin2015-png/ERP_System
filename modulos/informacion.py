from tkinter import *
from tkinter import ttk,messagebox,filedialog
import tkinter as tk
import especialidades.controlador as ctrl
import csv

class Informacion(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def widgets(self):
       
        #administrador

        labeladmin = tk.LabelFrame(self, text="Perfil del Administrador", font="arial 16 bold", bg="#C6D9E3")
        labeladmin.place(x=20, y=20, width=580, height=500)

        label_user = tk.Label(labeladmin, text="Usuario (Login): ", font="arial 14 bold", bg="#C6D9E3")
        label_user.place(x=10, y=10)
        self.entry_user = tk.Entry(labeladmin, font="arial 14")
        self.entry_user.place(x=250, y=10, width=250, height=30)

        label_pass = tk.Label(labeladmin, text="Contraseña: ", font="arial 14 bold", bg="#C6D9E3")
        label_pass.place(x=10, y=60)
        self.entry_pass = tk.Entry(labeladmin, font="arial 14", show="*")
        self.entry_pass.place(x=250, y=60, width=250, height=30)

        label_admin_nombre = tk.Label(labeladmin, text="Nombre Completo: ", font="arial 14 bold", bg="#C6D9E3")
        label_admin_nombre.place(x=10, y=110)
        self.entry_admin_nombre = tk.Entry(labeladmin, font="arial 14")
        self.entry_admin_nombre.place(x=250, y=110, width=250, height=30)

        label_admin_cedula = tk.Label(labeladmin, text="Cédula / ID: ", font="arial 14 bold", bg="#C6D9E3")
        label_admin_cedula.place(x=10, y=160)
        self.entry_admin_cedula = tk.Entry(labeladmin, font="arial 14")
        self.entry_admin_cedula.place(x=250, y=160, width=250, height=30)

        label_admin_telefono = tk.Label(labeladmin, text="Teléfono: ", font="arial 14 bold", bg="#C6D9E3")
        label_admin_telefono.place(x=10, y=210)
        self.entry_admin_telefono = tk.Entry(labeladmin, font="arial 14")
        self.entry_admin_telefono.place(x=250, y=210, width=250, height=30)

        label_admin_correo = tk.Label(labeladmin, text="Correo Electrónico: ", font="arial 14 bold", bg="#C6D9E3")
        label_admin_correo.place(x=10, y=260)
        self.entry_admin_correo = tk.Entry(labeladmin, font="arial 14")
        self.entry_admin_correo.place(x=250, y=260, width=250, height=30)

        self.boton_guardar_admin = tk.Button(labeladmin, text="Actualizar Perfil", font="arial 14 bold", bg="#4CAF50", fg="white", command=self.guardar_perfil_admin)
        self.boton_guardar_admin.place(x=10, y=410, width=460, height=40)

        #empleados

        labelemple=tk.LabelFrame(self,text="Nuevo Empleado",font="arial 14 bold",bg="#C6D9E3")
        labelemple.place(x=600,y=20,width=580,height=500)

        label_nom=tk.Label(labelemple,text="Nombre: ",font="arial 14 bold",bg="#C6D9E3")
        label_nom.place(x=10,y=10)
        self.entry_nom=tk.Entry(labelemple,font="arial 14 bold")
        self.entry_nom.place(x=250,y=10,width=250,height=30)

        label_ci=tk.Label(labelemple,text="Cedula: ",font="arial 14 bold",bg="#C6D9E3")
        label_ci.place(x=10,y=60)
        self.entry_ci=tk.Entry(labelemple,font="arial 14 bold")
        self.entry_ci.place(x=250,y=60,width=250,height=30)

        label_tel=tk.Label(labelemple,text="Teléfono: ",font="arial 14 bold",bg="#C6D9E3")
        label_tel.place(x=10,y=110)
        self.entry_tel=tk.Entry(labelemple,font="arial 14 bold")
        self.entry_tel.place(x=250,y=110,width=250,height=30)

        label_email=tk.Label(labelemple,text="Correo Electrónico: ",font="arial 14 bold",bg="#C6D9E3")
        label_email.place(x=10,y=160)
        self.entry_email=tk.Entry(labelemple,font="arial 14 bold")
        self.entry_email.place(x=250,y=160,width=250,height=30)

        label_rol=tk.Label(labelemple,text="Rol del Empleado: ",font="arial 14 bold",bg="#C6D9E3")
        label_rol.place(x=10,y=210)
        
        self.combo_rol = ttk.Combobox(labelemple, font="arial 14", state="readonly")
        self.combo_rol['values'] = ('Vendedor', 'Administrador', 'Tesorero', 'Encargado')
        self.combo_rol.current(0) 
        self.combo_rol.place(x=250, y=210, width=250)

        label_usu=tk.Label(labelemple,text="Usuario: ",font="arial 14 bold",bg="#C6D9E3")
        label_usu.place(x=10,y=260)
        self.entry_usu=tk.Entry(labelemple,font="arial 14 bold")
        self.entry_usu.place(x=250,y=260,width=250,height=30)

        label_passw=tk.Label(labelemple,text="Contraseña: ",font="arial 14 bold",bg="#C6D9E3")
        label_passw.place(x=10,y=310)
        self.entry_passw=tk.Entry(labelemple,font="arial 14 bold", show="*")
        self.entry_passw.place(x=250,y=310,width=250,height=30)

        label_sueldo=tk.Label(labelemple,text="Sueldo: ",font="arial 14 bold",bg="#C6D9E3")
        label_sueldo.place(x=10,y=360)
        self.entry_sueldo=tk.Entry(labelemple,font="arial 14 bold")
        self.entry_sueldo.place(x=250,y=360,width=250,height=30)

        self.boton_emple=tk.Button(labelemple,text="Agregar Empleado",font="arial 14 bold",bg="#2196F3",fg="white",command=self.guardar_nuevo_empleado)
        self.boton_emple.place(x=10, y=410, width=200, height=40)

        self.boton_ver_emple=tk.Button(labelemple,text="Ver Empleados",font="arial 14 bold",bg="#F44336",fg="white",command=self.ver_empleados)
        self.boton_ver_emple.place(x=220, y=410, width=200, height=40)

        #aparte
        self.boton_info=tk.Button(self,text="Informacion del negocio",font="arial 14 bold",bg="#BA48D6",fg="white",command=self.info_negocio)
        self.boton_info.place(x=20, y=540, width=400, height=40)

        self.cargar_perfil_existente()
    
    def guardar_nuevo_empleado(self):
        username = self.entry_usu.get().strip()
        password = self.entry_passw.get().strip()
        nombre   = self.entry_nom.get().strip()
        cedula   = self.entry_ci.get().strip()
        telefono = self.entry_tel.get().strip()
        correo   = self.entry_email.get().strip()
        rol      = self.combo_rol.get()
        sueldo_str = self.entry_sueldo.get().strip()

        if not username or not password or not sueldo_str:
            messagebox.showerror("Error", "Usuario, contraseña y sueldo son campos obligatorios.")
            return

        try:
            sueldo = float(sueldo_str)
            if sueldo < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce un sueldo numérico válido y positivo.")
            return

        exito, mensaje = ctrl.registrar_usuario(username, password, nombre, cedula, telefono, correo, rol, sueldo)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.entry_usu.delete(0, tk.END)
            self.entry_passw.delete(0, tk.END)
            self.entry_nom.delete(0, tk.END)
            self.entry_ci.delete(0, tk.END)
            self.entry_tel.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_sueldo.delete(0, tk.END)
            self.combo_rol.current(0)
            self.entry_usu.focus()

        else:
            messagebox.showerror("Error de Base de Datos", mensaje)

    def guardar_info_negocio(self):
        nom = self.entry_nombre.get()
        dir = self.entry_direccion.get()
        tel = self.entry_telefono.get()
        eml = self.entry_email.get()

        desc = self.text_descripcion.get("1.0", tk.END).strip()

        if nom == "":
            from tkinter import messagebox
            messagebox.showwarning("Atención", "El Nombre del Negocio es obligatorio.")
            return

        ctrl.guardar_empresa(nom, dir, tel, eml, desc)

        from tkinter import messagebox
        messagebox.showinfo("Éxito", "¡Información del negocio actualizada correctamente!")

    def ver_empleados(self):
        top_empleados = tk.Toplevel(self)
        top_empleados.title("Control de Empleados")
        top_empleados.geometry("950x600+300+80") 
        top_empleados.config(bg="#C6D9E3")
        top_empleados.resizable(False, False)
        top_empleados.transient(self.master)
        top_empleados.grab_set()

        self.filtro_rol_actual = "Todos"

        self.bt1 = tk.Button(top_empleados,  text="Mostrar Todo: Todos", font="arial 12 bold", bg="#4CAF50", fg="white", command=lambda: self.filtrar_por_rol())
        self.bt1.place(x=20, y=20, width=260, height=40) 

        self.bt2 = tk.Button(top_empleados, text="Descargar", font="arial 12 bold", bg="#2196F3", fg="white",command=lambda: descargar_empleados(self))
        self.bt2.place(x=300, y=20, width=220, height=40)

        canvas_finanzas = tk.Frame(top_empleados, bg="#C6D9E3")
        canvas_finanzas.place(x=20, y=80, width=910, height=500)

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

        self.canvas.create_window((0, 0), window=self.scrollbar_frame, anchor="nw", width=910)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.cargar_empleados()  
        self.filtro_rol_actual = "Todos" 

    def cargar_empleados(self, datos=None):
        if not hasattr(self, 'scrollbar_frame') or not self.scrollbar_frame.winfo_exists():
            return

        for widget in self.scrollbar_frame.winfo_children():
            widget.destroy()

        headers = ["ID", "Nombre Completo", "Cédula", "Rol", "Sueldo", "Acciones"]
        for col_idx, text in enumerate(headers):
            lbl_header = tk.Label(
                self.scrollbar_frame, text=text, font="arial 16 bold",
                bg="#9FB8C7", fg="black", relief="groove", pady=5
            )
            lbl_header.grid(row=0, column=col_idx, sticky="nsew")

        if datos is not None:
            lista_empleados = datos
        else:
            lista_empleados = ctrl.obtener_empleados()

        for row_idx, emp in enumerate(lista_empleados, start=1):
            id_emp, username, nombre, cedula, telefono, correo, rol, sueldo = emp

            if hasattr(self, 'filtro_rol_actual') and self.filtro_rol_actual != "Todos":
                if rol.strip().lower() != self.filtro_rol_actual.strip().lower():
                    continue

            color_fila = "#E1EBF0" if row_idx % 2 == 0 else "#F4F4F4"
            valores_fila = [id_emp, nombre, cedula, rol, sueldo]

            for col_idx, valor in enumerate(valores_fila):
                if col_idx == 4:
                    try:
                        sueldo_numero = float(valor)
                        texto_celda = f"${sueldo_numero:,.2f}"
                    except (ValueError, TypeError):
                        texto_celda = f"${valor}" if valor else "$0.00"
                else:
                    texto_celda = valor

                if col_idx in [0, 2, 3]:
                    anchor_val = "center"
                elif col_idx == 1:
                    anchor_val = "w"
                else:
                    anchor_val = "e"

                lbl_dato = tk.Label(
                    self.scrollbar_frame,
                    text=texto_celda,
                    font=("arial", 16),
                    bg=color_fila,
                    anchor=anchor_val,
                    padx=10,
                    pady=5
                )
                lbl_dato.grid(row=row_idx, column=col_idx, sticky="nsew")

            frame_botones = tk.Frame(self.scrollbar_frame, bg=color_fila)
            frame_botones.grid(row=row_idx, column=5, sticky="nsew", padx=1, pady=1)

            if id_emp != 1:
                frame_botones.columnconfigure(0, weight=1)
                
                btn_opciones = tk.Button(
                    frame_botones,
                    text="Opciones ▾",
                    bg="#4A5568", fg="white", 
                    font=("arial", 12, "bold"), bd=0,
                    width=10, cursor="hand2"
                )
                btn_opciones.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

                def desplegar_menu_empleado(b=btn_opciones, e=emp, id_b=id_emp, nom_b=nombre):
                    menu_popup = tk.Menu(b, tearoff=0, font=("arial", 11), bg="white", fg="black", activebackground="#2196F3")
                    
                    menu_popup.add_command(label="✏️ Editar", command=lambda: self.modificar_empleado_ventana(e))
                    menu_popup.add_command(label="🗑️ Eliminar", command=lambda: self.eliminar_empleado_accion(id_b, nom_b))
                    
                    # Posicionar el menú exactamente debajo del botón de opciones
                    x = b.winfo_rootx()
                    y = b.winfo_rooty() + b.winfo_height()
                    menu_popup.post(x, y)

                btn_opciones.config(command=desplegar_menu_empleado)

        self.scrollbar_frame.grid_columnconfigure(0, weight=1)
        self.scrollbar_frame.grid_columnconfigure(1, weight=3)
        self.scrollbar_frame.grid_columnconfigure(2, weight=2)  
        self.scrollbar_frame.grid_columnconfigure(3, weight=2)  
        self.scrollbar_frame.grid_columnconfigure(4, weight=2) 
        self.scrollbar_frame.grid_columnconfigure(5, weight=2) 

    def filtrar_por_rol(self):
        roles = ["Todos", "Vendedor", "Administrador", "Tesorero", "Encargado"]
        
        idx_actual = roles.index(self.filtro_rol_actual)
        idx_siguiente = (idx_actual + 1) % len(roles)
        
        self.filtro_rol_actual = roles[idx_siguiente]
        
        self.bt1.config(text=f"Mostrar Todo: {self.filtro_rol_actual}")
        
        self.cargar_empleados()

    def eliminar_empleado_accion(self, id_empleado, nombre_empleado):
        confirmacion = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar al empleado '{nombre_empleado}'?")
        if confirmacion:
            exito, mensaje = ctrl.eliminar_usuario(id_empleado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.cargar_empleados()
            else:
                messagebox.showerror("Error", mensaje)

    def modificar_empleado_ventana(self, datos_empleado):
        id_emp, username, nombre, cedula, telefono, correo, rol, sueldo = datos_empleado

        top_modificar = tk.Toplevel(self)
        top_modificar.title(f"Modificar Empleado: {username}")
        top_modificar.geometry("400x450+550+150")
        top_modificar.config(bg="#C6D9E3")
        top_modificar.grab_set()

        tk.Label(top_modificar, text="Nombre Completo:", font="arial 10 bold", bg="#C6D9E3").place(y=20, x=10)
        entry_nom = tk.Entry(top_modificar, font="arial 11")
        entry_nom.insert(0, nombre)
        entry_nom.place(x=10, y=45, width=380, height=30)
        tk.Label(top_modificar, text="Rol del Empleado:", font="arial 10 bold", bg="#C6D9E3").place(y=80, x=10)
        combo_r = ttk.Combobox(top_modificar, font="arial 11", state="readonly")
        combo_r['values'] = ('Vendedor', 'Administrador', 'Tesorero', 'Encargado')
        combo_r.set(rol)
        combo_r.place(y=105, x=10, width=380, height=30)

        tk.Label(top_modificar, text="Sueldo:", font="arial 10 bold", bg="#C6D9E3").place(y=140, x=10)
        entry_sld = tk.Entry(top_modificar, font="arial 11")
        entry_sld.insert(0, sueldo)
        entry_sld.place(x=10, y=165, width=380, height=30)

        def guardar_cambios():
            nuevo_nom = entry_nom.get().strip()
            nuevo_rol = combo_r.get()
            nuevo_sld = entry_sld.get().strip()

            if not nuevo_nom or not nuevo_sld:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                sueldo_float = float(nuevo_sld)
            except ValueError:
                messagebox.showerror("Error", "El sueldo debe ser un número válido.")
                return

            # Enviar actualización al controlador
            exito, mensaje = ctrl.actualizar_usuario(id_emp, nuevo_nom, nuevo_rol, sueldo_float)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                top_modificar.destroy()
                self.cargar_empleados() 
            else:
                messagebox.showerror("Error", mensaje)

        btn_guardar = tk.Button(
            top_modificar, 
            text="Guardar Cambios", 
            bg="#4CAF50", 
            fg="white", 
            font="arial 11 bold", 
            command=guardar_cambios
        )
        btn_guardar.place(x=10, y=220, width=380, height=40)

    def cargar_perfil_existente(self):
        registro = ctrl.obtener_perfil_admin()
        
        if registro is not None:
            self.entry_user.insert(0, registro[0])
            self.entry_pass.insert(0, registro[1])
            
            if registro[2]: self.entry_admin_nombre.insert(0, registro[2])
            if registro[3]: self.entry_admin_cedula.insert(0, registro[3])
            if registro[4]: self.entry_admin_telefono.insert(0, registro[4])
            if registro[5]: self.entry_admin_correo.insert(0, registro[5])

    def guardar_perfil_admin(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()
        nom = self.entry_admin_nombre.get()
        ced = self.entry_admin_cedula.get()
        tel = self.entry_admin_telefono.get()
        corr = self.entry_admin_correo.get()

        if user == "" or password == "":
            from tkinter import messagebox
            messagebox.showwarning("Atención", "El usuario y la contraseña no pueden estar vacíos.")
            return

        # Guardar en la base de datos sobre el ID 1
        exito = ctrl.actualizar_perfil_admin(user, password, nom, ced, tel, corr)
        
        from tkinter import messagebox
        if exito:
            messagebox.showinfo("Éxito", "¡Perfil de administrador actualizado correctamente!")
        else:
            messagebox.showerror("Error", "No se pudieron guardar los cambios en la base de datos.")    

    def info_negocio(self):
        toplabel = tk.Toplevel(self)
        toplabel.title("Información del Negocio")
        toplabel.geometry("750x600+450+80")
        toplabel.config(bg="#C6D9E3")
        toplabel.resizable(False, False)
        toplabel.transient(self.master)
        toplabel.grab_set()

        labelinformacion=tk.LabelFrame(toplabel,text="Información del Negocio",font="arial 16 bold",bg="#C6D9E3")
        labelinformacion.place(x=20,y=20,width=565,height=500)

        label_nombre=tk.Label(labelinformacion,text="Nombre del Negocio: ",font="arial 14 bold",bg="#C6D9E3")
        label_nombre.place(x=10,y=10)

        self.entry_nombre=tk.Entry(labelinformacion,font="arial 14")
        self.entry_nombre.place(x=250,y=10,width=250,height=30)

        label_direccion=tk.Label(labelinformacion,text="Dirección: ",font="arial 14 bold",bg="#C6D9E3")
        label_direccion.place(x=10,y=60)

        self.entry_direccion=tk.Entry(labelinformacion,font="arial 14")
        self.entry_direccion.place(x=250,y=60,width=250,height=30)

        label_telefono=tk.Label(labelinformacion,text="Teléfono: ",font="arial 14 bold",bg="#C6D9E3")
        label_telefono.place(x=10,y=110)

        self.entry_telefono=tk.Entry(labelinformacion,font="arial 14")
        self.entry_telefono.place(x=250,y=110,width=250,height=30)

        label_email=tk.Label(labelinformacion,text="Email: ",font="arial 14 bold",bg="#C6D9E3")
        label_email.place(x=10,y=160)

        self.entry_email=tk.Entry(labelinformacion,font="arial 14")
        self.entry_email.place(x=250,y=160,width=250,height=30)

        label_descripcion=tk.Label(labelinformacion,text="Descripción: ",font="arial 14 bold",bg="#C6D9E3")
        label_descripcion.place(x=10,y=210)

        self.text_descripcion=tk.Text(labelinformacion,font="arial 14")
        self.text_descripcion.place(x=250,y=210,width=250,height=100)

        self.boton_guardar=tk.Button(labelinformacion,text="Guardar Información",font="arial 14 bold",bg="#4CAF50",fg="white", command=self.guardar_info_negocio)
        self.boton_guardar.place(x=10, y=410, width=460, height=40)

        self.cargar_datos_existentes()
         
    def cargar_datos_existentes(self):
        registro = ctrl.obtener_empresa()
        
        if registro is not None:
            self.entry_nombre.insert(0, registro[0])
            self.entry_direccion.insert(0, registro[1])
            self.entry_telefono.insert(0, registro[2])
            self.entry_email.insert(0, registro[3])
            
            self.text_descripcion.delete("1.0", tk.END)
            self.text_descripcion.insert("1.0", registro[4])
            
            self.boton_guardar.config(text="Actualizar Información", bg="#2196F3") 
        else:
            self.boton_guardar.config(text="Guardar Información", bg="#4CAF50")

def descargar_empleados(self):
    empleados = ctrl.obtener_empleados()
    
    if not empleados:
        messagebox.showwarning("Advertencia", "No hay empleados registrados para exportar.")
        return

    ruta_archivo = filedialog.asksaveasfilename(
        title="Guardar Reporte de Empleados",
        defaultextension=".csv",
        filetypes=[("Archivos CSV (Excel)", "*.csv"), ("Todos los archivos", "*.*")]
    )
    
    if not ruta_archivo:
        return

    try:
        with open(ruta_archivo, mode='w', newline='', encoding='utf-8-sig') as archivo_csv:
            escritor = csv.writer(archivo_csv, delimiter=';') 
            
            escritor.writerow(["ID", "Usuario", "Nombre Completo", "Cédula", "Teléfono", "Correo", "Rol", "Sueldo"])
            
            for emp in empleados:
                id_emp, username, nombre, cedula, telefono, correo, rol, sueldo = emp
                
                sueldo_formateado = f"{float(sueldo):.2f}" if sueldo else "0.00"
                
                escritor.writerow([id_emp, username, nombre, cedula, telefono, correo, rol, sueldo_formateado])
                
        messagebox.showinfo("Éxito", f"Reporte exportado correctamente en:\n{ruta_archivo}")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo. Asegúrate de que no esté abierto en Excel.\nDetalle: {str(e)}")
