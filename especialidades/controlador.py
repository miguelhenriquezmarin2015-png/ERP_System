#import mysql.connector as sql
import mysql.connector
import configparser
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os
import sys
import csv

"""al terminar el programa cambiar de base de datos mysql por ende cambiar: sql.connect('negocio.db') por conectar() 
y cambiar los ? por %s en las consultas"""

#iniciar----

#def conectar():
 #   """Establece la conexión de red con la computadora servidor local."""
  #  return conectar(
   #     host="192.168.1.50",     # <-- La dirección IP local de la computadora Servidor/se tiene que cambiar segun la computadora en la que este la base de datos
    #    user="root",             # Usuario por defecto de tu servidor local (XAMPP/Laragon)
     #   password="",             # Contraseña por defecto (vacía en XAMPP)
      #  database="negocio_db"   
    #)
def obtener_ruta_config():
    if getattr(sys, 'frozen', False):
        directorio_base = os.path.dirname(sys.executable)
    else:    
        directorio_base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(directorio_base, 'config.ini')

def conectar():
    try:
        config = configparser.ConfigParser()
        ruta_config = obtener_ruta_config()
        config.read(ruta_config)

        conexion = mysql.connector.connect(
            host=config['BASEDATOS']['IP_SERVIDOR'],
            user=config['BASEDATOS']['Usuario'],
            password=config["BASEDATOS"]['Clave'],
            database=config["BASEDATOS"]['NombreDB']
        )

        return conexion
    except Exception as e:
        print(f"Error crítico al conectar a la base de datos: {e}")
        return None

#Creción de base de datos

def crear_base_de_datos():
    try:
        config = configparser.ConfigParser()
        ruta_config = obtener_ruta_config()
        config.read(ruta_config)
        conexion = mysql.connector.connect(
            host=config['BASEDATOS']['IP_SERVIDOR'],
            user=config['BASEDATOS']['Usuario'],
            password=config["BASEDATOS"]['Clave']
        )
        cursor = conexion.cursor()
        nombre_db = config["BASEDATOS"]['NombreDB']
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre_db}")
        cursor.execute(f"USE {nombre_db}")

        tablas = [
            "CREATE TABLE IF NOT EXISTS empresa ( id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255) NOT NULL, direccion TEXT, telefono VARCHAR(50), email VARCHAR(100), descripcion TEXT )",
            "CREATE TABLE IF NOT EXISTS clientes ( id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255) NOT NULL, cedula VARCHAR(50) NOT NULL, telefono VARCHAR(50) NOT NULL, tipo VARCHAR(50) NOT NULL DEFAULT 'Natural' )",
            "CREATE TABLE IF NOT EXISTS usuarios ( id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL, nombre VARCHAR(255), cedula VARCHAR(50), telefono VARCHAR(50), correo VARCHAR(100), rol VARCHAR(50) NOT NULL DEFAULT 'Vendedor', sueldo DECIMAL(10,2) NOT NULL DEFAULT 0.0 )",
            "CREATE TABLE IF NOT EXISTS ventas ( id INT AUTO_INCREMENT PRIMARY KEY, numero_factura VARCHAR(50) NOT NULL UNIQUE, cliente VARCHAR(255) NOT NULL, fecha DATETIME NOT NULL, total DECIMAL(12,2) NOT NULL )",
            "CREATE TABLE IF NOT EXISTS detalles_ventas ( id INT AUTO_INCREMENT PRIMARY KEY, venta_id INT NOT NULL, producto VARCHAR(255) NOT NULL, precio_unitario DECIMAL(10,2) NOT NULL, cantidad INT NOT NULL, subtotal DECIMAL(12,2) NOT NULL, FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE )",
            "CREATE TABLE IF NOT EXISTS inventario ( id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255) NOT NULL UNIQUE, costo DECIMAL(10,2) NOT NULL, precio DECIMAL(10,2) NOT NULL, stock INT NOT NULL, perecedero TINYINT(1) NOT NULL DEFAULT 0, vencimiento DATE )",
            "CREATE TABLE IF NOT EXISTS proveedores ( id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255) NOT NULL, rif VARCHAR(50) NOT NULL UNIQUE, contacto VARCHAR(255) NOT NULL )",
            "CREATE TABLE IF NOT EXISTS proveedor_catalogo ( id_proveedor INT NOT NULL, id_producto INT NOT NULL, PRIMARY KEY(id_proveedor, id_producto), FOREIGN KEY(id_proveedor) REFERENCES proveedores(id) ON DELETE CASCADE, FOREIGN KEY(id_producto) REFERENCES inventario(id) ON DELETE CASCADE )",
            "CREATE TABLE IF NOT EXISTS compras_proveedor ( id INT AUTO_INCREMENT PRIMARY KEY, id_proveedor INT NOT NULL, fecha DATETIME NOT NULL, total_pagado DECIMAL(12,2) NOT NULL, detalles TEXT, FOREIGN KEY(id_proveedor) REFERENCES proveedores(id) ON DELETE CASCADE )",
            "CREATE TABLE IF NOT EXISTS pedidos_pendientes ( id INT AUTO_INCREMENT PRIMARY KEY, id_proveedor INT NOT NULL, producto VARCHAR(255) NOT NULL, cantidad INT NOT NULL, monto_estimado DECIMAL(12,2) NOT NULL, estado VARCHAR(50) NOT NULL DEFAULT 'Pendiente', FOREIGN KEY(id_proveedor) REFERENCES proveedores(id) ON DELETE CASCADE )"
        ]
        for tabla in tablas:
            cursor.execute(tabla)

        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES ('admin', 'admin123', 'Administrador')") 
        conexion.commit()
        conexion.close()

    except Exception as e:
        print(f"Error en la instalación de la base de datos: {e}")


#inventario -------

def guardar_articulo(nombre,costo,precio,stock,perecedero,vencimiento):
    conn = conectar()
    cursor = conn.cursor()
    if vencimiento== 'No Aplica'or not vencimiento:
        vencimiento = None
    instruccion="INSERT INTO inventario (nombre, costo, precio, stock, perecedero, vencimiento) VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(instruccion, (nombre, costo, precio, stock, perecedero, vencimiento))
    conn.commit()
    conn.close()

def obtener_articulos():
    conn = conectar()
    cursor = conn.cursor()
    try:
        query = "SELECT id, nombre, costo, precio, stock, perecedero, vencimiento FROM inventario;"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error en ctrl.obtener_articulos: {e}")
        return []
    finally:
        conn.close()


def buscar_articulo(nombre):
    conn = conectar()
    cursor = conn.cursor()
    instruccion="SELECT * FROM inventario where nombre LIKE %s"
    termino_busqueda = f"%{nombre}%"
    cursor.execute(instruccion, (termino_busqueda,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def mostrar_vender(nombre):
    conn = conectar()
    cursor = conn.cursor()
    instruccion = "SELECT costo, precio, stock FROM inventario WHERE nombre = %s"
    cursor.execute(instruccion, (nombre,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado 

def mostrar_inventario_baja_cantidad():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventario WHERE stock < 15")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def obtener_productos_por_vencer():
    conn = conectar()
    cursor = conn.cursor()
    try:
        query = """
            SELECT nombre, vencimiento 
            FROM inventario 
            WHERE perecedero = 1 
              AND vencimiento IS NOT NULL 
              AND vencimiento <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
              AND vencimiento >= CURDATE();
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al verificar vencimientos: {str(e)}")
        return []
    finally:
        conn.close()

def actualizar_articulo(id, nombre, costo, precio, stock, perecedero,vencimiento):
    conn = conectar()
    cursor = conn.cursor()
    if vencimiento == 'No Aplica' or not vencimiento:
        vencimiento = None
    instruccion = "UPDATE inventario SET nombre = %s, costo = %s, precio = %s, stock = %s, perecedero = %s, vencimiento = %s WHERE id = %s"
    cursor.execute(instruccion, (nombre, costo, precio, stock, perecedero,vencimiento, id))
    conn.commit()
    conn.close()

def reducir_stock(nombre, cantidad):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT stock FROM inventario WHERE nombre = %s", (nombre,))
        resultado = cursor.fetchone()
        
        if resultado:
            stock_actual = resultado[0]
            nuevo_stock = stock_actual - cantidad
            
            cursor.execute("UPDATE inventario SET stock = %s WHERE nombre = %s", (nuevo_stock, nombre))
            conn.commit()
            print(f"Stock actualizado para {nombre}: {nuevo_stock}")
            
    except Exception as e:
        conn.rollback()
        print(f"Error al reducir stock: {e}")
        
    finally:
        conn.close()

def restaurar_stock(nombre, cantidad):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT stock FROM inventario WHERE nombre = %s", (nombre,))
        resultado = cursor.fetchone()
        if resultado:
            nuevo_stock = resultado[0] + cantidad
            cursor.execute("UPDATE inventario SET stock = %s WHERE nombre = %s", (nuevo_stock, nombre))
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error al restaurar stock: {e}")
    finally:
        conn.close()
   
def obtener_stock_actual(nombre_producto):
    conexion = conectar()
    cursor = conexion.cursor()
    
    query = "SELECT stock FROM inventario WHERE nombre = %s"
    cursor.execute(query, (nombre_producto,))
    resultado = cursor.fetchone()
    
    conexion.close()
    
    return resultado[0] if resultado else 0

def eliminar_articulo(id):
    conn = conectar()
    cursor = conn.cursor()
    instruccion="DELETE FROM inventario WHERE id=%s"
    cursor.execute(instruccion, (id,))
    conn.commit()
    conn.close()

#usuario-----

def buscar_usuario(username):
    conn = conectar()
    cursor = conn.cursor()
    instruccion="SELECT * FROM usuarios where username LIKE %s"
    termino_busqueda = f"%{username}%"
    cursor.execute(instruccion, (termino_busqueda,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def registrar_usuario(username, password, nombre, cedula, telefono, correo, rol, sueldo):
    conexion = conectar()
    cursor = conexion.cursor()
    
    intruccion= """
    INSERT INTO usuarios (username, password, nombre, cedula, telefono, correo, rol, sueldo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    try:
        cursor.execute(intruccion, (username, password, nombre, cedula, telefono, correo, rol, sueldo))
        conexion.commit()
        return True, f"Empleado '{username}' registrado correctamente."
        
    except mysql.connector.IntegrityError:
        return False, f"El nombre de usuario '{username}' ya existe en el sistema."
        
    except Exception as e:
        return False, f"Ocurrió un error inesperado: {str(e)}"
        
    finally:
        conexion.close()

def obtener_empleados():
    conexion = conectar()
    cursor = conexion.cursor()
    
    query = "SELECT id, username, nombre, cedula, telefono, correo, rol, sueldo FROM usuarios;"
    
    try:
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"Error al consultar empleados: {str(e)}")
        return []
    finally:
        conexion.close()

def eliminar_usuario(id_usuario):
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE id = %s;", (id_usuario,))
        conexion.commit()
        return True, "Empleado eliminado correctamente."
    except Exception as e:
        return False, f"No se pudo eliminar: {str(e)}"
    finally:
        conexion.close()

def actualizar_usuario(id_usuario, nombre, rol, sueldo):
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE usuarios 
            SET nombre = %s, rol = %s, sueldo = %s 
            WHERE id = %s;
        """, (nombre, rol, sueldo, id_usuario))
        conexion.commit()
        return True, "Datos del empleado actualizados con éxito."
    except Exception as e:
        return False, f"Error al actualizar: {str(e)}"
    finally:
        conexion.close()

def validacion(usuario, contrasena):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password, rol FROM usuarios WHERE username = %s", (usuario,))

        resultado = cursor.fetchone()
        
        if resultado:
            db_password = resultado[0]
            db_rol = resultado[1]
            
            if db_password == contrasena:
                return str(db_rol).strip()
                
        return None
    except Exception as e:
        print(f"Error en validación: {str(e)}")
        return None
    finally:
        conn.close()

#empresa-----

def guardar_empresa(nombre, direccion, telefono, email, descripcion):
    conn = conectar()
    cursor = conn.cursor()
    instruccion = """INSERT INTO empresa (id, nombre, direccion, telefono, email, descripcion)
                     VALUES (1, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE nombre=VALUES(nombre), direccion=VALUES(direccion),
                     telefono=VALUES(telefono), email=VALUES(email), descripcion=VALUES(descripcion);"""
    cursor.execute(instruccion, (nombre, direccion, telefono, email, descripcion))
    conn.commit()
    conn.close()

def obtener_empresa():
    conn = conectar()
    cursor = conn.cursor()
    instruccion = "SELECT nombre, direccion, telefono, email, descripcion FROM empresa WHERE id = 1"
    cursor.execute(instruccion)
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def obtener_perfil_admin():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, nombre, cedula, telefono, correo FROM usuarios WHERE id = 1")
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def actualizar_perfil_admin(usuario, contrasena, nombre, cedula, telefono, correo):
    conn = conectar()
    cursor = conn.cursor()
    instruccion = """UPDATE usuarios 
                     SET username=%s, password=%s, nombre=%s, cedula=%s, telefono=%s, correo=%s 
                     WHERE id = 1"""
    cursor.execute(instruccion, (usuario, contrasena, nombre, cedula, telefono, correo))
    conn.commit()
    conn.close()

#ventas-----
def exportar_ventas_pdf(modo):
    conexion = conectar()
    cursor = conexion.cursor()
    query = "SELECT id, numero_factura, cliente, fecha, total FROM ventas"
    condicion = ""

    if modo == "Diario":
        condicion = " WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 1 DAY)"
    elif modo == "Semanal":
        condicion = " WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
    elif modo == "Quincenal":
        condicion = " WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 15 DAY)"
    elif modo == "Mensual":
        condicion = " WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 30  DAY)"
    else:
        condicion = "" 
        
    cursor.execute(query + condicion + " ORDER BY id DESC")
    datos_ventas = cursor.fetchall()
    conexion.close()

    carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    nombre_archivo = f"Reporte_{modo}.pdf"
    ruta_destino_completa = os.path.join(carpeta_descargas, nombre_archivo)

    doc = SimpleDocTemplate(ruta_destino_completa, pagesize=letter)
    elementos = []
    
    # Definición de los estilos de fuentes y espaciados
    estilos = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle('Titulo', parent=estilos['Heading1'], fontSize=24, leading=28, textColor=colors.HexColor("#2196F3"), spaceAfter=12)
    estilo_sub = ParagraphStyle('Sub', parent=estilos['Normal'], fontSize=12, leading=16, spaceAfter=20)

    # Estructura del encabezado del documento
    elementos.append(Paragraph("REPORTE DE VENTAS", estilo_titulo))
    elementos.append(Paragraph(f"Filtro aplicado: {modo} | Historial generado automáticamente en Descargas.", estilo_sub))
    elementos.append(Spacer(1, 10))

    tabla_datos = [["ID", "N° Factura", "Cliente", "Fecha", "Total"]]
    total_acumulado = 0.0

    for v in datos_ventas:
        total_acumulado += float(v[4])
        fila_formateada = [str(v[0]), str(v[1]), str(v[2]), str(v[3]), f"${v[4]:,.2f}"]
        tabla_datos.append(fila_formateada)

    tabla_datos.append(["", "", "", "TOTAL:", f"${total_acumulado:,.2f}"])

    tabla_pdf = Table(tabla_datos, colWidths=[40, 80, 200, 100, 100])
    
    estilo_tabla = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#9FB8C7")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),  
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),  
        ('ALIGN', (4, 0), (4, -1), 'RIGHT'),  
        ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
    ])

    for i in range(1, len(tabla_datos) - 1):
        bg_color = colors.HexColor("#E1EBF0") if i % 2 == 0 else colors.HexColor("#F4F8FA")
        estilo_tabla.add('BACKGROUND', (0, i), (-1, i), bg_color)

    tabla_pdf.setStyle(estilo_tabla)
    elementos.append(tabla_pdf)

    doc.build(elementos)
    #hola que hace
    return ruta_destino_completa

def guardar_venta_completa(numero_factura, cliente, lista_productos, total):
    """
    Guarda de forma segura la cabecera y todos los productos asociados 
    dentro de una misma transacción SQL.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        instruccion_venta = "INSERT INTO ventas (numero_factura, cliente, fecha, total) VALUES (%s, %s, NOW(), %s)"
        cursor.execute(instruccion_venta, (numero_factura, cliente, total))
        
        venta_id = cursor.lastrowid        
        instruccion_detalle = """
            INSERT INTO detalles_ventas (venta_id, producto, precio_unitario, cantidad, subtotal) 
            VALUES (%s, %s, %s, %s, %s)
        """ 
        datos_detalles = []
        for producto, precio, cantidad, subtotal in lista_productos:
            datos_detalles.append((venta_id, producto, precio, cantidad, subtotal))
            
        cursor.executemany(instruccion_detalle, datos_detalles)
        conn.commit()
        print("¡La venta completa se registró con total éxito!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error crítico al guardar la venta: {e}")
        raise e
        
    finally:
        conn.close()

def obtener_num_factura():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT numero_factura FROM ventas ORDER BY id DESC LIMIT 1")
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        ultimo_numero = resultado[0]
        nuevo_numero = int(ultimo_numero) + 1
        return str(nuevo_numero).zfill(6)
    else:
        return "01"
    
def cargar_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM inventario")
    productos = cursor.fetchall()
    conn.close()
    return [producto[0] for producto in productos]

def filtrar_nombre(texto_busqueda):
    conn = conectar()
    cursor = conn.cursor()
    instruccion = "SELECT nombre FROM inventario WHERE nombre LIKE %s ORDER BY nombre ASC"
    termino = f"%{texto_busqueda}%"
    cursor.execute(instruccion, (termino,))
    resultados = cursor.fetchall()
    conn.close()    
    return [producto[0] for producto in resultados]

def obtener_ventas():
    conexion = conectar()
    cursor = conexion.cursor()    
    query = "SELECT id, numero_factura, cliente, fecha, total FROM ventas ORDER BY id DESC"
    cursor.execute(query)
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

def obtener_ventas_filtradas(modo):
    conexion = conectar()
    cursor = conexion.cursor()

    query = "SELECT id, numero_factura, cliente, fecha, total FROM ventas"
    condicion = ""

    if modo == "Diario":
        condicion = " WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 1 DAY)"
    elif modo == "Semanal":
        condicion = " WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
    elif modo == "Quincenal":
        condicion = " WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 15 DAY)"
    elif modo == "Mensual":
        condicion = " WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)"
    else:
        condicion = ""

    query_final = query + condicion + " ORDER BY id DESC"
    cursor.execute(query_final)
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

#clientes-----

def guardar_cliente(nombre, telefono, cedula, tipo):
    conn = conectar()
    cursor = conn.cursor()
    instruccion="INSERT INTO clientes (nombre, telefono, cedula, tipo) VALUES (%s, %s, %s, %s)"
    cursor.execute(instruccion, (nombre, telefono, cedula, tipo))
    conn.commit()
    conn.close()

def obtener_clientes():
    conexion = conectar()
    cursor = conexion.cursor()
    query = "SELECT id, nombre, cedula, telefono, tipo FROM clientes"
    cursor.execute(query)
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

def modificar_cliente(id_cliente, nombre, telefono, cedula, tipo):
    conexion = conectar()
    cursor = conexion.cursor()    
    query = """
        UPDATE clientes 
        SET nombre = %s, telefono = %s, cedula = %s, tipo = %s 
        WHERE id = %s
    """
    cursor.execute(query, (nombre, telefono, cedula, tipo, id_cliente))
    conexion.commit()
    conexion.close()

def buscar_cliente(nombre):
    conn = conectar()
    cursor = conn.cursor()
    instruccion="SELECT * FROM clientes where nombre LIKE %s"
    termino_busqueda = f"%{nombre}%"
    cursor.execute(instruccion, (termino_busqueda,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def filtrar_clientes_por_nombre(texto_busqueda):
    conn = conectar()
    cursor = conn.cursor()
    instruccion = "SELECT nombre FROM clientes WHERE nombre LIKE %s ORDER BY nombre ASC"
    termino = f"%{texto_busqueda}%"
    cursor.execute(instruccion, (termino,))
    resultados = cursor.fetchall()
    conn.close()
    return [cliente[0] for cliente in resultados]

def obtener_nombres_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM clientes ORDER BY nombre ASC")
    resultados = cursor.fetchall()
    conn.close()

    lista_clientes = [cliente[0] for cliente in resultados]
    return lista_clientes

def tipo_cliente(nombre_cliente):
    conexion = conectar()
    cursor = conexion.cursor()
    
    query = "SELECT tipo FROM clientes WHERE nombre = %s"
    cursor.execute(query, (nombre_cliente,))
    resultado = cursor.fetchone()
    
    conexion.close()
    
    return resultado[0] if resultado else 'Natural'

#proveedores----
def obtener_proveedores():
    
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nombre, rif, contacto FROM proveedores;")
        return cursor.fetchall() # Devuelve las tuplas completas de 4 elementos
    except Exception as e:
        print(f"Error al consultar proveedores: {str(e)}")
        return []
    finally:
        conn.close()

def obtener_nombres_proveedores():
    
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nombre FROM proveedores ORDER BY nombre ASC")
        resultados = cursor.fetchall()
        return [f"{prov[0]} - {prov[1]}" for prov in resultados] # Devuelve texto
    except Exception as e:
        print(f"Error al consultar nombres de proveedores: {str(e)}")
        return []
    finally:
        conn.close()

def registrar_proveedor_db(nombre, rif, contacto):
    conn = conectar()
    cursor = conn.cursor()
    
    query = "INSERT INTO proveedores (nombre, rif, contacto) VALUES (%s, %s, %s);"
    
    try:
        cursor.execute(query, (nombre, rif, contacto))
        conn.commit()
        return True, f"Proveedor '{nombre}' registrado con éxito."
    except mysql.connector.IntegrityError:
        return False, f"El RIF '{rif}' ya se encuentra registrado en el sistema."
    except Exception as e:
        return False, f"Error en la base de datos: {str(e)}"
    finally:
        conn.close()

def agregar_producto_a_catalogo(id_proveedor, nombre, costo, precio, perecedero, vencimiento):
    conn = conectar()
    cursor = conn.cursor()
    try:
        fecha_sql = None if (vencimiento == "" or vencimiento == "No Aplica") else vencimiento

        query_inventario = """
            INSERT INTO inventario (nombre, costo, precio, stock, perecedero, vencimiento) 
            VALUES (%s, %s, %s, 0, %s, %s)
            ON DUPLICATE KEY UPDATE 
                costo = VALUES(costo), 
                precio = VALUES(precio), 
                perecedero = VALUES(perecedero), 
                vencimiento = VALUES(vencimiento);
        """
        cursor.execute(query_inventario, (nombre, costo, precio, int(perecedero), fecha_sql))
        
        cursor.execute("SELECT id FROM inventario WHERE nombre = %s;", (nombre,))
        id_producto = cursor.fetchone()[0]

        query_catalogo = """
            INSERT IGNORE INTO proveedor_catalogo (id_proveedor, id_producto) 
            VALUES (%s, %s);
        """
        cursor.execute(query_catalogo, (id_proveedor, id_producto))

        conn.commit()
        return True, "¡Artículo guardado exitosamente en catálogo e inventario!"
        
    except Exception as e:
        conn.rollback()
        print(f"Error relacional en base de datos: {e}")
        return False, f"Error en la base de datos: {e}"
    finally:
        conn.close()

def obtener_catalogo_por_proveedor(id_proveedor):
    conn = conectar()
    cursor = conn.cursor()
    try:
        query = """
            SELECT pc.id_producto, i.nombre, i.costo, i.precio, i.stock, i.perecedero, i.vencimiento
            FROM proveedor_catalogo pc
            INNER JOIN inventario i ON pc.id_producto = i.id
            WHERE pc.id_proveedor = %s;
        """
        cursor.execute(query, (id_proveedor,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error en ctrl.obtener_catalogo_por_proveedor: {e}")
        return []
    finally:
        conn.close()

def obtener_compras_proveedor(id_proveedor):
    conn = conectar()
    cursor = conn.cursor()
    try:
        query = "SELECT id, fecha, total_pagado, detalles FROM compras_proveedor WHERE id_proveedor = %s;"
        cursor.execute(query, (id_proveedor,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error en obtener_compras_proveedor: {e}") 
        return []
    finally:
        conn.close()

def obtener_pedidos_pendientes(id_proveedor):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, producto, cantidad, monto_estimado, estado FROM pedidos_pendientes WHERE id_proveedor = %s AND estado = 'Pendiente';", (id_proveedor,))
        return cursor.fetchall()
    except Exception:
        return []
    finally:
        conn.close()

def recibir_pedido_pendiente_db(id_pedido):
    conn = conectar()
    cursor = conn.cursor()
    try:
        query_select = "SELECT id_proveedor, monto_estimado, producto, cantidad FROM pedidos_pendientes WHERE id = %s;"
        cursor.execute(query_select, (id_pedido,))
        pedido = cursor.fetchone()
        
        if pedido:
            id_prov, monto_estimado, producto, cantidad_recibida = pedido
            nota_historial = f"Pedido Recibido: {producto}"
            
            query_insert = """
                INSERT INTO compras_proveedor (id_proveedor, fecha, total_pagado, detalles) 
                VALUES (%s, NOW(), %s, %s);
            """
            cursor.execute(query_insert, (id_prov, monto_estimado, nota_historial))
            
            query_buscar_inv = "SELECT stock FROM inventario WHERE nombre = %s;"
            cursor.execute(query_buscar_inv, (producto,))
            item_inventario = cursor.fetchone()
            
            if item_inventario:
                stock_actual = item_inventario[0]
                nuevo_stock = stock_actual + cantidad_recibida
                query_update_inv = "UPDATE inventario SET stock = %s WHERE nombre = %s;"
                cursor.execute(query_update_inv, (nuevo_stock, producto))
            else:
                costo_unitario = monto_estimado / cantidad_recibida if cantidad_recibida > 0 else 0
                query_crear_inv = """
                    INSERT INTO inventario (nombre, costo, precio, stock, perecedero, vencimiento) 
                    VALUES (%s, %s, 0.00, %s, 0, NULL);
                """
                cursor.execute(query_crear_inv, (producto, costo_unitario, cantidad_recibida))
            
            query_delete = "DELETE FROM pedidos_pendientes WHERE id = %s;"
            cursor.execute(query_delete, (id_pedido,))
            
            conn.commit()
            return True
            
        return False
        
    except Exception as e:
        conn.rollback()
        print(f"Error en ctrl.recibir_pedido_pendiente_db con inventario: {e}")
        return False
    finally:
        conn.close()

def actualizar_articulo_catalogo(id_producto, nombre, costo, precio, perecedero, vencimiento):
    conn = conectar()
    cursor = conn.cursor()
    try:
        fecha_sql = None if (vencimiento == "No Aplica" or vencimiento == "") else vencimiento
        
        query = """
            UPDATE inventario 
            SET nombre = %s, costo = %s, precio = %s, perecedero = %s, vencimiento = %s 
            WHERE id = %s;
        """
        cursor.execute(query, (nombre, costo, precio, int(perecedero), fecha_sql, id_producto))
        conn.commit()
        return True, "¡Artículo actualizado con éxito!"
    except Exception as e:
        conn.rollback()
        print(f"Error al actualizar artículo: {e}")
        return False, f"Error: {e}"
    finally:
        conn.close()


def guardar_pedido_bd(id_proveedor, lista_productos):
    conn = conectar()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO pedidos_pendientes (id_proveedor, producto, cantidad, monto_estimado, estado) VALUES (%s, %s, %s, %s, 'Pendiente')"
        for prod in lista_productos:
            total_estimado = float(prod['cantidad']) * float(prod['costo'])
            cursor.execute(query, (id_proveedor, prod['nombre'], prod['cantidad'], total_estimado))
        conn.commit()
        return True, "El pedido fue registrado con éxito."
    except Exception as e:
        return False, f"Error al guardar el pedido: {str(e)}"
    finally:
        conn.close()

def generar_orden_pedido_pdf(nombre_proveedor, lista_productos, total_general):
    carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    fecha_actual= datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"Orden_Pedido_{nombre_proveedor.replace(' ','_')}_{fecha_actual}.pdf"
    ruta_destino = os.path.join(carpeta_descargas, nombre_archivo)

    documento= SimpleDocTemplate(ruta_destino, pagesize=letter)
    elementos = []
    estilos =getSampleStyleSheet()

    titulo = ParagraphStyle('Titulo', parent=estilos['Heading1'], fontSize=20, textColor=colors.HexColor("#2196F3"))
    elementos.append(Paragraph(f"ORDEN DE COMPRA", titulo))
    elementos.append(Paragraph(f"<b>Proveedor:</b> {nombre_proveedor} | <b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilos['Normal']))
    elementos.append(Spacer(1, 20))

    tabla_datos = [["Producto / Artículo", "Cantidad", "Costo Unitario","Subtotal"]]
    for p in lista_productos:
        subtotal = p['cantidad']* float(p['costo'])
        tabla_datos.append([p['nombre'], str(p['cantidad']), f"${p['costo']:.2f}", f"${subtotal:.2f}"])
    
    tabla_datos.append(["","", "TOTAL:", f"${total_general:.2f}"])

    tabla_pdf= Table(tabla_datos, colWidths=[250, 80, 100, 100])
    tabla_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#9FB8C7")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-2), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (-2,-1), (-1,-1), 'Helvetica-Bold'),
    ]))

    elementos.append(tabla_pdf)
    documento.build(elementos)
    return ruta_destino

def generar_csv_pedido(nombre_proveedor, lista_productos, total_general):
    carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"Orden_Pedido_{nombre_proveedor.replace(' ', '_')}_{fecha_actual}.csv"
    ruta_destino = os.path.join(carpeta_descargas, nombre_archivo)

    with open(ruta_destino, mode="w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f, delimiter=";")
        escritor.writerow(["Proveedor:", nombre_proveedor, "Fecha:", datetime.now().strftime('%d/%m/%Y %H:%M')])
        escritor.writerow([])
        escritor.writerow(["Producto / Artículo", "Cantidad", "Costo Unitario", "Subtotal"])
        
        for p in lista_productos:
            subtotal = p['cantidad'] * float(p['costo'])
            escritor.writerow([p['nombre'], p['cantidad'], f"${p['costo']:.2f}", f"${subtotal:.2f}"])
            
        escritor.writerow([])
        escritor.writerow(["", "", "TOTAL DE LA ORDEN:", f"${total_general:.2f}"])
        
    return ruta_destino