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

def cadastrar_cliente(tipo, nome, telefone, email, cpf_cnpj):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cliente (tipo, nome, telefone, email, cpf_cnpj) VALUES (?, ?, ?, ?, ?)", (tipo, nome, telefone, email, cpf_cnpj))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente")
    dados = cursor.fetchall()
    conn.close()
    return dados

def deletar_cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cliente WHERE id = ?", (id_cliente,))
    conn.commit()
    conn.close()

def atualizar_cliente(id_cliente, tipo, nome, telefone, email, cpf_cnpj):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE cliente SET tipo = ?, nome = ?, telefone = ?, email = ?, cpf_cnpj = ? WHERE id = ?", (tipo, nome, telefone, email, cpf_cnpj, id_cliente))
    conn.commit()
    conn.close()  

def cadastrar_equipamento(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO equipamento (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def listar_equipamentos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipamento")
    dados = cursor.fetchall()
    conn.close()
    return dados

def deletar_equipamento(id_equipamento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM equipamento WHERE id = ?", (id_equipamento,))
    conn.commit()
    conn.close()

def atualizar_equipamento(id_equipamento, nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE equipamento SET nome = ? WHERE id = ?", (nome, id_equipamento))
    conn.commit()
    conn.close()  

def cadastrar_sala(nome, numero, andar, capacidade, observacoes, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sala (nome, numero, andar, capacidade, observacoes, status) VALUES (?, ?, ?, ?, ?, ?)", (nome, numero, andar, capacidade, observacoes, status))
    conn.commit()
    conn.close()

def listar_salas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sala")
    dados = cursor.fetchall()
    conn.close()
    return dados

def deletar_sala(id_sala):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sala WHERE id = ?", (id_sala,))
    conn.commit()
    conn.close()

def atualizar_sala(id_sala, nome, numero, andar, capacidade, observacoes, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE sala SET nome = ?, numero = ?, andar = ?, capacidade = ?, observacoes = ?, status = ? WHERE id = ?", (nome, numero, andar, capacidade, observacoes, status, id_sala))
    conn.commit()
    conn.close()  

def cadastrar_reserva(id_sala, id_cliente, data, hora_inicio, hora_fim, status, criado_em):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reserva (id_sala, id_cliente, data, hora_inicio, hora_fim, status, criado_em) VALUES (?, ?, ?, ?, ?, ?, ?)", (id_sala, id_cliente, data, hora_inicio, hora_fim, status, criado_em))
    conn.commit()
    conn.close()

def db_listar_reservas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT sala.nome,
                          cliente.nome,
                          reserva.data,
                          reserva.hora_inicio,
                          reserva.hora_fim,
                          reserva.status,
                          reserva.criado_em
                   FROM reserva
                   INNER JOIN sala ON reserva.id = sala.id
                   INNER JOIN cliente ON reserva.id = cliente.id
                  """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def db_deletar_reserva(id_reserva):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reserva WHERE id = ?", (id_reserva,))
    conn.commit()
    conn.close()

def db_atualizar_reserva(id_reserva, id_sala, id_cliente, data, hora_inicio, hora_fim, status, criado_em):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE reserva SET id_sala = ?, id_cliente = ?, data = ?, hora_inicio = ?, hora_fim = ?, status = ?, criado_em = ? WHERE id = ?", (id_sala, id_cliente, data, hora_inicio, hora_fim, status, criado_em, id_reserva))
    conn.commit()
    conn.close()

def cadastrar_sala_equipamento(id_sala, id_equipamento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sala_equipamento (id_sala, id_equipamento) VALUES (?, ?)", (id_sala, id_equipamento))
    conn.commit()
    conn.close()

def db_listar_sala_equipamento():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT sala.nome,
                          equipamento.nome
                   FROM sala_equipamento
                   INNER JOIN sala ON sala_equipamento.id_sala = sala.id
                   INNER JOIN equipamento ON sala_equipamento.id_equipamento = equipamento.id
                  """)
    dados = cursor.fetchall()
    conn.close()
    return dados

#Manipulação para o sistema do projeto




    




