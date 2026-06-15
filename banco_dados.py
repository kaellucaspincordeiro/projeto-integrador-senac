import sqlite3
import script_banco

def conectar():
    conn = sqlite3.connect("salas_reunioes.db")
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON;""")
    cursor.execute(script_banco.administrador)
    cursor.execute(script_banco.equipamento)
    cursor.execute(script_banco.cliente)
    cursor.execute(script_banco.sala)
    cursor.execute(script_banco.reserva)
    cursor.execute(script_banco.sala_equipamento)
    cursor.execute(script_banco.busca)
    conn.commit()
    return conn



