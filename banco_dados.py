import sqlite3

def conexao():
    conn = sqlite3.connect("salas_reunioes.db", timeout=10)
    conn.execute("""PRAGMA foreign_keys = ON;""")
    return conn

def inicializar_banco(on_status=None):
    conn = conexao()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS administrador (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            senha_hash TEXT NOT NULL,
                            pergunta_seguranca TEXT NOT NULL,
                            resposta_seguranca_hash TEXT NOT NULL)
                    """)
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS equipamento (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            nome TEXT NOT NULL UNIQUE)
                    """)
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sala (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            numero TEXT NOT NULL,
                            andar INTEGER NOT NULL CHECK (andar BETWEEN 1 AND 15),
                            capacidade INTEGER NOT NULL CHECK (capacidade > 0),
                            observacoes TEXT,
                            status TEXT NOT NULL DEFAULT 'ativa' CHECK (status IN ('ativa', 'manutencao'))
                            )
                    """)
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cliente (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            tipo TEXT NOT NULL CHECK (tipo IN ('F', 'J')),
                            nome TEXT NOT NULL,
                            telefone TEXT,
                            email TEXT,
                            cpf_cnpj TEXT NOT NULL UNIQUE)
                    """)
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sala_equipamento (
                            id_sala INTEGER NOT NULL,
                            id_equipamento INTEGER NOT NULL,
                            PRIMARY KEY (id_sala, id_equipamento),
                            CONSTRAINT fk_sala FOREIGN KEY (id_sala) REFERENCES sala (id) ON DELETE CASCADE,
                            CONSTRAINT fk_equipamento FOREIGN KEY (id_equipamento) REFERENCES equipamento (id) ON DELETE CASCADE
                    )
                    """)
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS reserva (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_sala INTEGER NOT NULL,
                            id_cliente INTEGER NOT NULL,
                            data TEXT NOT NULL,  -- formato AAAA-MM-DD
                            hora_inicio TEXT NOT NULL,  -- formato HH:MM
                            hora_fim TEXT NOT NULL,  -- formato HH:MM
                            status TEXT NOT NULL DEFAULT 'ativa'
                                    CHECK (status IN ('ativa', 'cancelada')),
                            criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                            CONSTRAINT fk_reserva_sala FOREIGN KEY (id_sala) REFERENCES sala (id),
                            CONSTRAINT fk_reserva_cliente FOREIGN KEY (id_cliente) REFERENCES cliente (id))
                    """)
        cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_reserva_sala_data ON reserva (id_sala, data, status);
                    """)
        conn.commit()

        if on_status:
            on_status("Banco inicializado com sucesso")

    except sqlite3.Error as erro:
        conn.rollback()

        if on_status:
            on_status("Erro para inicializar o banco")

        raise

    finally:
        conn.close()


def cadastrar_cliente(tipo, nome, telefone, email, cpf_cnpj):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cliente (tipo, nome, telefone, email, cpf_cnpj) VALUES (?, ?, ?, ?, ?)", (tipo, nome, telefone, email, cpf_cnpj))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente")
    dados = cursor.fetchall()
    conn.close()
    return dados

def deletar_cliente(id_cliente):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cliente WHERE id = ?", (id_cliente,))
    conn.commit()
    conn.close()

def atualizar_cliente(id_cliente, tipo, nome, telefone, email, cpf_cnpj):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE cliente SET tipo = ?, nome = ?, telefone = ?, email = ?, cpf_cnpj = ? WHERE id = ?", (tipo, nome, telefone, email, cpf_cnpj, id_cliente))
    conn.commit()
    conn.close()  

def cadastrar_equipamento(nome):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO equipamento (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def listar_equipamentos():
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipamento")
    dados = cursor.fetchall()
    conn.close()
    return dados

def deletar_equipamento(id_equipamento):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM equipamento WHERE id = ?", (id_equipamento,))
    conn.commit()
    conn.close()

def atualizar_equipamento(id_equipamento, nome):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE equipamento SET nome = ? WHERE id = ?", (nome, id_equipamento))
    conn.commit()
    conn.close()  

def cadastrar_sala(nome, numero, andar, capacidade, observacoes, status):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sala (nome, numero, andar, capacidade, observacoes, status) VALUES (?, ?, ?, ?, ?, ?)", (nome, numero, andar, capacidade, observacoes, status))
    conn.commit()
    conn.close()

def listar_salas():
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sala")
    dados = cursor.fetchall()
    conn.close()
    return dados

def deletar_sala(id_sala):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sala WHERE id = ?", (id_sala,))
    conn.commit()
    conn.close()

def atualizar_sala(id_sala, nome, numero, andar, capacidade, observacoes, status):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE sala SET nome = ?, numero = ?, andar = ?, capacidade = ?, observacoes = ?, status = ? WHERE id = ?", (nome, numero, andar, capacidade, observacoes, status, id_sala))
    conn.commit()
    conn.close()  

def cadastrar_reserva(id_sala, id_cliente, data, hora_inicio, hora_fim, status, criado_em):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reserva (id_sala, id_cliente, data, hora_inicio, hora_fim, status, criado_em) VALUES (?, ?, ?, ?, ?, ?, ?)", (id_sala, id_cliente, data, hora_inicio, hora_fim, status, criado_em))
    conn.commit()
    conn.close()

def db_listar_reservas():
    conn = conexao()
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
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reserva WHERE id = ?", (id_reserva,))
    conn.commit()
    conn.close()

def db_atualizar_reserva(id_reserva, id_sala, id_cliente, data, hora_inicio, hora_fim, status, criado_em):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE reserva SET id_sala = ?, id_cliente = ?, data = ?, hora_inicio = ?, hora_fim = ?, status = ?, criado_em = ? WHERE id = ?", (id_sala, id_cliente, data, hora_inicio, hora_fim, status, criado_em, id_reserva))
    conn.commit()
    conn.close()

def cadastrar_sala_equipamento(id_sala, id_equipamento):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sala_equipamento (id_sala, id_equipamento) VALUES (?, ?)", (id_sala, id_equipamento))
    conn.commit()
    conn.close()

def db_listar_sala_equipamento():
    conn = conexao()
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




    




