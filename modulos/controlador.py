import sqlite3 as sql
from datetime import datetime
#inventario -------
def createDB_Inventario():
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS inventario
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT NOT NULL,
                  costo REAL NOT NULL,
                  precio REAL NOT NULL,
                  stock INTEGER NOT NULL)""")
    conn.commit()
    conn.close()

def guardar_articulo(nombre,costo,precio,stock):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="INSERT INTO inventario (nombre, costo, precio, stock) VALUES (?,?,?,?)"
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
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="SELECT * FROM inventario where nombre LIKE ?"
    termino_busqueda = f"%{nombre}%"
    cursor.execute(instruccion, (termino_busqueda,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def mostrar_vender(nombre):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion = "SELECT costo, precio, stock FROM inventario WHERE nombre = ?"
    cursor.execute(instruccion, (nombre,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado 

def mostrar_inventario_baja_cantidad():
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventario WHERE stock < 15")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def actualizar_articulo(id, nombre, costo, precio, stock):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion = "UPDATE inventario SET nombre = ?, costo = ?, precio = ?, stock = ? WHERE id = ?"
    cursor.execute(instruccion, (nombre, costo, precio, stock, id))
    conn.commit()
    conn.close()

def reducir_stock(nombre, cantidad):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT stock FROM inventario WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()
        
        if resultado:
            stock_actual = resultado[0]
            nuevo_stock = stock_actual - cantidad
            
            cursor.execute("UPDATE inventario SET stock = ? WHERE nombre = ?", (nuevo_stock, nombre))
            conn.commit()
            print(f"Stock actualizado para {nombre}: {nuevo_stock}")
            
    except Exception as e:
        conn.rollback()
        print(f"Error al reducir stock: {e}")
        
    finally:
        conn.close()

def restaurar_stock(nombre, cantidad):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT stock FROM inventario WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()
        if resultado:
            nuevo_stock = resultado[0] + cantidad
            cursor.execute("UPDATE inventario SET stock = ? WHERE nombre = ?", (nuevo_stock, nombre))
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error al restaurar stock: {e}")
    finally:
        conn.close()

    
def eliminar_articulo(id):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="DELETE FROM inventario WHERE id=?"
    cursor.execute(instruccion, (id,))
    conn.commit()
    conn.close()

#usuario-----

def createDB_Usuario():
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def validacion(user,pas):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="SELECT * FROM usuarios where username=? and password=?"
    cursor.execute(instruccion, (user, pas))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def buscar_usuario(username):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="SELECT * FROM usuarios where username=?"
    termino_busqueda = f"%{username}%"
    cursor.execute(instruccion, (termino_busqueda,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

#ventas-----
def createDB_Ventas():
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS ventas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  numero_factura TEXT NOT NULL,
                  cliente TEXT NOT NULL,
                  fecha NUMERIC NOT NULL,
                  total REAL NOT NULL)""")
    conn.commit()
    conn.close()

def createDB_Detalles_Ventas():
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS detalles_ventas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  numero_factura TEXT NOT NULL,
                  producto TEXT NOT NULL,
                  precio_unitario REAL NOT NULL,
                  cantidad INTEGER NOT NULL,
                  subtotal REAL NOT NULL)""")
    conn.commit()
    conn.close()

def guardar_venta_completa(numero_factura, cliente, lista_productos, total):
    """
    Guarda de forma segura la cabecera y todos los productos asociados 
    dentro de una misma transacción SQL.
    """
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    
    try:
        instruccion_venta = "INSERT INTO ventas (numero_factura, cliente, fecha, total) VALUES (?, ?, datetime('now', 'localtime'), ?)"
        cursor.execute(instruccion_venta, (numero_factura, cliente, total))
        
        venta_id = cursor.lastrowid        
        instruccion_detalle = """
            INSERT INTO detalles_ventas (venta_id, producto, precio_unitario, cantidad, subtotal) 
            VALUES (?, ?, ?, ?, ?)
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
    conn = sql.connect('negocio.db')
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
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM inventario")
    productos = cursor.fetchall()
    conn.close()
    return [producto[0] for producto in productos]

#clientes-----

def createDB_Clientes():
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT NOT NULL,
                  telefono TEXT NOT NULL,
                  cedula TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def guardar_cliente(nombre, telefono, cedula):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="INSERT INTO clientes (nombre, telefono, cedula) VALUES (?,?,?)"
    cursor.execute(instruccion, (nombre, telefono, cedula))
    conn.commit()
    conn.close()

def buscar_cliente(nombre):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="SELECT * FROM clientes where nombre LIKE ?"
    termino_busqueda = f"%{nombre}%"
    cursor.execute(instruccion, (termino_busqueda,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def obtener_nombres_clientes():
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM clientes ORDER BY nombre ASC")
    resultados = cursor.fetchall()
    conn.close()
    
    lista_clientes = [cliente[0] for cliente in resultados]
    return lista_clientes