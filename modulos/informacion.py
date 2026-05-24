from tkinter import *
import tkinter as tk
import modulos.controlador as ctrl

class Informacion(tk.Frame):
    def __init__(self, padre,controller):
        super().__init__(padre)
        self.controller=controller
        self.widgets()

    def widgets(self):

        labelinformacion=tk.LabelFrame(self,text="Información del Negocio",font="arial 16 bold",bg="#C6D9E3")
        labelinformacion.place(x=20,y=20,width=490,height=500)

        label_nombre=tk.Label(labelinformacion,text="Nombre del Negocio: ",font="arial 14 bold",bg="#C6D9E3")
        label_nombre.place(x=10,y=10)

        self.entry_nombre=tk.Entry(labelinformacion,font="arial 14")
        self.entry_nombre.place(x=250,y=10,width=220,height=30)

        label_direccion=tk.Label(labelinformacion,text="Dirección: ",font="arial 14 bold",bg="#C6D9E3")
        label_direccion.place(x=10,y=60)

        self.entry_direccion=tk.Entry(labelinformacion,font="arial 14")
        self.entry_direccion.place(x=250,y=60,width=220,height=30)

        label_telefono=tk.Label(labelinformacion,text="Teléfono: ",font="arial 14 bold",bg="#C6D9E3")
        label_telefono.place(x=10,y=110)

        self.entry_telefono=tk.Entry(labelinformacion,font="arial 14")
        self.entry_telefono.place(x=250,y=110,width=220,height=30)

        label_email=tk.Label(labelinformacion,text="Email: ",font="arial 14 bold",bg="#C6D9E3")
        label_email.place(x=10,y=160)

        self.entry_email=tk.Entry(labelinformacion,font="arial 14")
        self.entry_email.place(x=250,y=160,width=220,height=30)

        label_descripcion=tk.Label(labelinformacion,text="Descripción: ",font="arial 14 bold",bg="#C6D9E3")
        label_descripcion.place(x=10,y=210)

        self.text_descripcion=tk.Text(labelinformacion,font="arial 14")
        self.text_descripcion.place(x=250,y=210,width=220,height=100)

        self.boton_guardar=tk.Button(labelinformacion,text="Guardar Información",font="arial 14 bold",bg="#4CAF50",fg="white", command=self.guardar_info_negocio)
        self.boton_guardar.place(x=10,y=350,width=200,height=40)
        
        #administrador

        labeladmin = tk.LabelFrame(self, text="Perfil del Administrador", font="arial 16 bold", bg="#C6D9E3")
        labeladmin.place(x=530, y=20, width=490, height=500)

        label_user = tk.Label(labeladmin, text="Usuario (Login): ", font="arial 14 bold", bg="#C6D9E3")
        label_user.place(x=10, y=10)
        self.entry_user = tk.Entry(labeladmin, font="arial 14")
        self.entry_user.place(x=250, y=10, width=220, height=30)

        label_pass = tk.Label(labeladmin, text="Contraseña: ", font="arial 14 bold", bg="#C6D9E3")
        label_pass.place(x=10, y=60)
        self.entry_pass = tk.Entry(labeladmin, font="arial 14", show="*")
        self.entry_pass.place(x=250, y=60, width=220, height=30)

        label_admin_nombre = tk.Label(labeladmin, text="Nombre Completo: ", font="arial 14 bold", bg="#C6D9E3")
        label_admin_nombre.place(x=10, y=110)
        self.entry_admin_nombre = tk.Entry(labeladmin, font="arial 14")
        self.entry_admin_nombre.place(x=250, y=110, width=220, height=30)

        label_admin_cedula = tk.Label(labeladmin, text="Cédula / ID: ", font="arial 14 bold", bg="#C6D9E3")
        label_admin_cedula.place(x=10, y=160)
        self.entry_admin_cedula = tk.Entry(labeladmin, font="arial 14")
        self.entry_admin_cedula.place(x=250, y=160, width=220, height=30)

        label_admin_telefono = tk.Label(labeladmin, text="Teléfono: ", font="arial 14 bold", bg="#C6D9E3")
        label_admin_telefono.place(x=10, y=210)
        self.entry_admin_telefono = tk.Entry(labeladmin, font="arial 14")
        self.entry_admin_telefono.place(x=250, y=210, width=220, height=30)

        label_admin_correo = tk.Label(labeladmin, text="Correo Electrónico: ", font="arial 14 bold", bg="#C6D9E3")
        label_admin_correo.place(x=10, y=260)
        self.entry_admin_correo = tk.Entry(labeladmin, font="arial 14")
        self.entry_admin_correo.place(x=250, y=260, width=220, height=30)

        self.boton_guardar_admin = tk.Button(labeladmin, text="Actualizar Perfil", font="arial 14 bold", bg="#2196F3", fg="white", command=self.guardar_perfil_admin)
        self.boton_guardar_admin.place(x=10, y=410, width=460, height=40)

        self.cargar_datos_existentes()

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
        ctrl.actualizar_perfil_admin(user, password, nom, ced, tel, corr)

        from tkinter import messagebox
        messagebox.showinfo("Éxito", "¡Perfil de administrador actualizado correctamente!")


