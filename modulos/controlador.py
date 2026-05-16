import sqlite3 as sql
#inventario -------
def createDB_Inventario():
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS inventario
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT NOT NULL,
                  precio REAL NOT NULL,
                  stock INTEGER NOT NULL)""")
    conn.commit()
    conn.close()

def guardar_articulo(nombre,precio,stock):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="INSERT INTO inventario (nombre, precio, stock) VALUES (?,?,?)"
    cursor.execute(instruccion, (nombre, precio, stock))
    conn.commit()
    conn.close()

def mostrar_id(id):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="SELECT * FROM inventario where id=?"
    cursor.execute(instruccion, (id,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def obtener_articulos():
    conn = sql.connect("negocio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio, stock FROM inventario")
    articulos = cursor.fetchall()
    conn.close()
    return articulos

def mostrar_inventario_baja_cantidad():
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventario WHERE stock < 15")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def editar_articulo(id,stock):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="UPDATE inventario SET stock=? WHERE id=?"
    cursor.execute(instruccion, (stock, id))
    conn.commit()
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


#createDB_Inventario()
#createDB_Usuario()