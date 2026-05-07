import sqlite3 as sql
import inventario.py
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
    instruccion=f"INSERT INTO inventario (nombre, cantidad, precio) VALUES ('{get_nombre()}')"
    cursor.execute(*instruccion)
    conn.commit()
    conn.close()
