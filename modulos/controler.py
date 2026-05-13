import sqlite3 as sql
#inventario -------
def createDB_Inventario():
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS inventario
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT NOT NULL,
                  cantidad INTEGER NOT NULL,
                  precio REAL NOT NULL)""")
    conn.commit()
    conn.close()

def insertar_inventario(nombre,cantidad,precio):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="INSERT INTO inventario (nombre, cantidad, precio) VALUES (?,?,?)"
    cursor.execute(instruccion, (nombre, cantidad, precio))
    conn.commit()
    conn.close()

def mostar_id(id):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="SELECT * FROM inventario where id=?"
    cursor.execute(instruccion, (id,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def mostrar_inventario_baja_cantidad():
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventario WHERE cantidad < 15")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def update_inventario(id,cantidad):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    instruccion="UPDATE inventario SET cantidad=? WHERE id=?"
    cursor.execute(instruccion, (cantidad, id))
    conn.commit()
    conn.close()

#usuario-----

def createDB_Usuario():
    conn = sql.connect('usuario.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def validacion(user,pas):
    conn = sql.connect('usuario.db')
    cursor = conn.cursor()
    instruccion="SELECT * FROM usuarios where username=? and password=?"
    cursor.execute(instruccion, (user, pas))
    resultado = cursor.fetchall()
    conn.close()
    return resultado


#createDB_Inventario()
#createDB_Usuario()