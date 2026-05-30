import os
import sys
import configparser
import tkinter as tk
from tkinter import messagebox, simpledialog
import urllib.request
import threading

if getattr(sys, 'frozen', False):
    directorio_base = os.path.dirname(sys.executable)
else:
    directorio_base = os.path.dirname(__file__)

ruta_config = os.path.join(directorio_base, 'config.ini')
#Asistente de primer inicio 
def primer_inicio():
    root = tk.Tk()
    root.title("Configuración Inicial del ERP")
    root.geometry("450x280")
    root.eval('tk::PlaceWindow . center')
    root.configure(bg="#f4f4f4")

    tk.Label(root, text="¡Bienvenido al ERP!", font=("Helvetica", 16, "bold"), bg="#f4f4f4").pack(pady=15)
    tk.Label(root, text="Parece que es la primera vez que ejecutas el programa.\n¿Qué función cumplirá este equipo?", justify="center", bg="#f4f4f4").pack(pady=10)

    def guardar_configuracion(ip):
        config = configparser.ConfigParser()
        config['BASEDATOS'] = {'IP_SERVIDOR': ip, 'Usuario': 'root', 'Clave':'','NombreDB': 'erp_negocio'}
        with open(ruta_config, 'w') as configfile:
            config.write(configfile)
    def set_servidor():
        guardar_configuracion('localhost')
        respuesta = messagebox.askyesno("Servidor Principal", "Para funcionar como Servidor, necesitas instalar la base de datos,\n\n¿Deseas instalar Laragon?")
        if respuesta:
            descargar_laragon(root)
        else:
            messagebox.showinfo("Listo", "Configración guardada. Recuerde abrir y encender Laragon antes de abrir el programa.")
            root.destroy()

    def set_cliente():
        ip = simpledialog.askstring("Equipo Afiliado", "Ingresa la dirección IP del Servidor Principal\n(Ejemplo: 192.168.0.11):", parent=root)
        if ip:
            guardar_configuracion(ip.strip())
            messagebox.showinfo("Listo", f"Equipo configurado como Afiliado a {ip}.\nConectando...")
            root.destroy()
    tk.Button(root, text="1. Servidor Principal", width=35, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=set_servidor).pack(pady=8)
    tk.Button(root, text="2. Equipo Afiliado", width=35, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), command=set_cliente).pack(pady=8)

    root.mainloop()

def descargar_laragon(parent):
    top = tk.Toplevel(parent)
    top.title("Descargando...")
    top.geometry("350x120")
    top.eval('tk::PlaceWindow . center')

    lbl_progreso = tk.Label(top, text="Iniciando descarga de Laragon (170MB)...", font=("Helvetica", 10))
    lbl_progreso.pack(pady=30)
    
    def reporthook(bloque_num, tamano_bloque, tamano_total):
        if tamano_total > 0:
            porcentaje = min(int(bloque_num * tamano_bloque *100 / tamano_total), 100)
            top.after(0, lambda: lbl_progreso.config(text=f"Descargando instalador... {porcentaje}%"))

    def descargar():
        enlace =  "https://github.com/leokhoa/laragon/releases/download/6.0.0/laragon-wamp.exe"
        destino = os.path.join(os.path.expanduser("~"), "Downloads", "laragon-wamp.exe")
        try:
            urllib.request.urlretrieve(enlace, destino, reporthook)
            top.after(0, lambda: finalizar_descarga(destino))
        except Exception as e:
            top.after (0, lambda: error_descarga(e))

    def finalizar_descarga(destino):
        messagebox.showinfo("Descarga Completada", "Luego de instalar y abrir Laragon, presiona 'Iniciar Todo' y vuelve a iniciar este programa\nAbriendo instalador de Laragon...")
        os.startfile(destino)
        sys.exit()

    def error_descarga(e):
        messagebox.showerror("Error", f"No se pudo descargar Laragon:\n{e}\n\nPor favor, descarga e instala Laragon manualmente desde:\nhttps://laragon.org/download/index.html")
        sys.exit()



if __name__=="__main__":
    if not os.path.exists(ruta_config):
        primer_inicio()
    if not os.path.exists(ruta_config):
        sys.exit()
    from especialidades.controlador import crear_base_de_datos
    from especialidades.manager import Manager
    try:
        crear_base_de_datos()
    except Exception as e:
        print(f"Aviso BD:{e}")
    app=Manager()
    app.mainloop()