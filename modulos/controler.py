import sqlite3 as sql
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
    instruccion=f"INSERT INTO inventario (nombre, cantidad, precio) VALUES ('{nombre}', {cantidad}, {precio})"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def mostar_id(id):
    conn = sql.connect('negocio.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventario where id={id}")
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
    instruccion=f"UPDATE inventario SET cantidad={cantidad} WHERE id={id}"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()