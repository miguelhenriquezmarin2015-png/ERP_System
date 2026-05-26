import mysql.connector as sql
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os

#iniciar----

def conectar():
    """Establece la conexión de red con la computadora servidor local."""
    return sql.connect(
        host="192.168.1.50",     # <-- La dirección IP local de la computadora Servidor/se tiene que cambiar segun la computadora en la que este la base de datos
        user="root",             # Usuario por defecto de tu servidor local (XAMPP/Laragon)
        password="",             # Contraseña por defecto (vacía en XAMPP)
        database="negocio_db"   
    )

def create_all_tables():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "empresa" (
        "id"          INTEGER NOT NULL,
        "nombre"      TEXT NOT NULL,
        "direccion"   TEXT,
        "telefono"    TEXT,
        "email"       TEXT,
        "descripcion" TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "clientes" (
        "id"       INTEGER NOT NULL,
        "nombre"   TEXT NOT NULL,
        "cedula"   TEXT NOT NULL,
        "telefono" TEXT NOT NULL,
        "tipo"     TEXT NOT NULL DEFAULT 'Natural',
        PRIMARY KEY("id" AUTOINCREMENT)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "usuarios" (
        "id"              INTEGER NOT NULL,
        "username"        TEXT NOT NULL UNIQUE,
        "password"        TEXT NOT NULL,
        "nombre"          TEXT,
        "cedula"          TEXT,
        "telefono"        TEXT,
        "correo"          TEXT,
        "rol"             TEXT NOT NULL DEFAULT 'Vendedor',
        PRIMARY KEY("id" AUTOINCREMENT)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "ventas" (
        "id"             INTEGER NOT NULL,
        "numero_factura" TEXT NOT NULL UNIQUE,
        "cliente"        TEXT NOT NULL,
        "fecha"          NUMERIC NOT NULL,
        "total"          REAL NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "detalles_ventas" (
        "id"              INTEGER NOT NULL,
        "venta_id"        INTEGER NOT NULL,
        "producto"        TEXT NOT NULL,
        "precio_unitario" REAL NOT NULL,
        "cantidad"        INTEGER NOT NULL,
        "subtotal"        INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT),
        CONSTRAINT "ventas" FOREIGN KEY("venta_id") REFERENCES "ventas"("id")
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "inventario" (
        "id"     INTEGER NOT NULL,
        "nombre" TEXT NOT NULL,
        "costo"  REAL NOT NULL,
        "precio" REAL NOT NULL,
        "stock"  INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
    );
    """)

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO usuarios (id, username, password, rol) 
        VALUES (1, 'admin', 'admin', 'Administrador')
        """)

    conn.commit()
    conn.close()

create_all_tables()

#inventario -------

def guardar_articulo(nombre,costo,precio,stock):
    conn = conectar()
    cursor = conn.cursor()
    instruccion="INSERT INTO inventario (nombre, costo, precio, stock) VALUES (%s,%s,%s,%s)"
    cursor.execute(instruccion, (nombre, costo, precio, stock))
    conn.commit()
    conn.close()

def obtener_articulos():
    conn = sql.connect("negocio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, costo, precio, stock FROM inventario")
    articulos = cursor.fetchall()
    conn.close()
    return articulos

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

def actualizar_articulo(id, nombre, costo, precio, stock):
    conn = conectar()
    cursor = conn.cursor()
    instruccion = "UPDATE inventario SET nombre = %s, costo = %s, precio = %s, stock = %s WHERE id = %s"
    cursor.execute(instruccion, (nombre, costo, precio, stock, id))
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

def validacion(user,pas):
    conn = conectar()
    cursor = conn.cursor()
    instruccion="SELECT * FROM usuarios where username=%s and password=%s"
    cursor.execute(instruccion, (user, pas))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def buscar_usuario(username):
    conn = conectar()
    cursor = conn.cursor()
    instruccion="SELECT * FROM usuarios where username LIKE %s"
    termino_busqueda = f"%{username}%"
    cursor.execute(instruccion, (termino_busqueda,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado


#empresa-----

def guardar_empresa(nombre, direccion, telefono, email, descripcion):
    conn = conectar()
    cursor = conn.cursor()
    instruccion = """INSERT OR REPLACE INTO empresa (id, nombre, direccion, telefono, email, descripcion)
                     VALUES (1, %s, %s, %s, %s, %s)"""
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
    """Recupera los datos completos del usuario principal (ID = 1)."""
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
    conexion = sql.connect("negocio.db")
    cursor = conexion.cursor()
    query = "SELECT id, numero_factura, cliente, fecha, total FROM ventas"
    condicion = ""

    if modo == "Diario":
        condicion = " WHERE fecha >= date('now', '-1 day')"
    elif modo == "Semanal":
        condicion = " WHERE fecha >= date('now', '-7 days')"
    elif modo == "Quincenal":
        condicion = " WHERE fecha >= date('now', '-15 days')"
    elif modo == "Mensual":
        condicion = " WHERE fecha >= date('now', '-30 days')"
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
    
    return ruta_destino_completa

def guardar_venta_completa(numero_factura, cliente, lista_productos, total):
    """
    Guarda de forma segura la cabecera y todos los productos asociados 
    dentro de una misma transacción SQL.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        instruccion_venta = "INSERT INTO ventas (numero_factura, cliente, fecha, total) VALUES (%s, %s, datetime('now', 'localtime'), %s)"
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
    conexion = sql.connect("negocio.db")
    cursor = conexion.cursor()    
    query = "SELECT id, numero_factura, cliente, fecha, total FROM ventas ORDER BY id DESC"
    cursor.execute(query)
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

def obtener_ventas_filtradas(modo):
    conexion = sql.connect("negocio.db")
    cursor = conexion.cursor()

    query = "SELECT id, numero_factura, cliente, fecha, total FROM ventas"
    condicion = ""

    if modo == "Diario":
        condicion = " WHERE fecha >= date('now', '-1 day')"
    elif modo == "Semanal":
        condicion = " WHERE fecha >= date('now', '-7 days')"
    elif modo == "Quincenal":
        condicion = " WHERE fecha >= date('now', '-15 days')"
    elif modo == "Mensual":
        condicion = " WHERE fecha >= date('now', '-30 days')"

    query_final = query + condicion + " ORDER BY id DESC"
    cursor.execute(query_final)
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

#clientes-----

def guardar_cliente(nombre, telefono, cedula, tipo):
    conn = conectar()
    cursor = conn.cursor()
    instruccion="INSERT INTO clientes (nombre, telefono, cedula, tipo) VALUES (%s,%s,%s,%s)"
    cursor.execute(instruccion, (nombre, telefono, cedula, tipo))
    conn.commit()
    conn.close()

def obtener_clientes():
    conexion = sql.connect("negocio.db")
    cursor = conexion.cursor()
    query = "SELECT id, nombre, cedula, telefono, tipo FROM clientes"
    cursor.execute(query)
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

def modificar_cliente(id_cliente, nombre, telefono, cedula, tipo):
    conexion = sql.connect("negocio.db")
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
