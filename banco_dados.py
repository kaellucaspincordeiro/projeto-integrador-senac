import sqlite3

#Melhoria Feita por Kael:
#Adicionando o atributo quantidade_disponivel na tabela equipamento,
#correção na inserção e atualização do equipamento.
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
                            nome TEXT NOT NULL UNIQUE,
                            quantidade_disponivel INTEGER NOT NULL)
                    """)
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sala (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            numero TEXT NOT NULL,
                            andar INTEGER NOT NULL CHECK (andar BETWEEN 1 AND 15),
                            capacidade INTEGER NOT NULL CHECK (capacidade > 0),
                            observacoes TEXT,
                            status TEXT NOT NULL DEFAULT 'disponivel' CHECK (status IN ('disponivel', 'indisponivel', 'manutencao'))
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
                            quantidade INTEGER NOT NULL DEFAULT 1 CHECK (quantidade > 0),
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

        # ----------------------------------------------------------------
        # MIGRACOES (Dener) - bancos criados por versoes antigas do projeto
        # nao tinham algumas colunas que o codigo de hoje ja usa. Como o
        # "CREATE TABLE IF NOT EXISTS" nao mexe numa tabela que ja existe,
        # aqui a gente adiciona as colunas que faltarem, sem perder os dados.
        # ----------------------------------------------------------------
        def _garantir_coluna(tabela, coluna, definicao):
            colunas = [c[1] for c in cursor.execute(f"PRAGMA table_info({tabela})").fetchall()]
            if coluna not in colunas:
                cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {definicao}")

        _garantir_coluna("equipamento", "quantidade_disponivel", "INTEGER NOT NULL DEFAULT 0")
        _garantir_coluna("sala_equipamento", "quantidade", "INTEGER NOT NULL DEFAULT 1")

        # Migracao do CHECK de status da tabela 'sala'.
        # Versoes antigas criaram o status com CHECK ('ativa', 'manutencao').
        # Hoje o sistema usa 'disponivel'/'indisponivel'/'manutencao'. Como o SQLite
        # nao deixa alterar um CHECK com ALTER TABLE, recriamos a tabela copiando os
        # dados (trocando o antigo 'ativa' por 'disponivel'). So roda se for preciso.
        sql_sala = cursor.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='sala'"
        ).fetchone()
        if sql_sala and "disponivel" not in sql_sala[0]:
            cursor.execute("""
                        CREATE TABLE sala_migrada (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT NOT NULL,
                                numero TEXT NOT NULL,
                                andar INTEGER NOT NULL CHECK (andar BETWEEN 1 AND 15),
                                capacidade INTEGER NOT NULL CHECK (capacidade > 0),
                                observacoes TEXT,
                                status TEXT NOT NULL DEFAULT 'disponivel'
                                        CHECK (status IN ('disponivel', 'indisponivel', 'manutencao')))
                        """)
            cursor.execute("""
                        INSERT INTO sala_migrada (id, nome, numero, andar, capacidade, observacoes, status)
                        SELECT id, nome, numero, andar, capacidade, observacoes,
                               CASE status WHEN 'ativa' THEN 'disponivel' ELSE status END
                        FROM sala
                        """)
            cursor.execute("DROP TABLE sala")
            cursor.execute("ALTER TABLE sala_migrada RENAME TO sala")

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


# Melhoria feita por Dener em 17/06/2026
# Antes, se eu tentasse cadastrar um cliente com um CPF/CNPJ que ja existe (essa coluna e UNIQUE),
# o programa quebrava e fechava na cara do usuario.
# Coloquei um try/except para "segurar" esse erro: se o CPF/CNPJ ja existir, a funcao devolve False
# em vez de quebrar; se der tudo certo, devolve True. Assim a tela consegue avisar o usuario.
# O "finally" garante que a conexao com o banco sempre seja fechada, dando certo ou errado.
def cadastrar_cliente(tipo, nome, telefone, email, cpf_cnpj):
    conn = conexao()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO cliente (tipo, nome, telefone, email, cpf_cnpj) VALUES (?, ?, ?, ?, ?)", (tipo, nome, telefone, email, cpf_cnpj))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False
    finally:
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

# Melhoria feita por Dener em 17/06/2026
# O nome do equipamento e UNIQUE no banco, ou seja, nao pode repetir.
# Antes, tentar cadastrar um equipamento com nome repetido quebrava o programa.
# Agora o try/except devolve False se ja existir e True se cadastrar certinho.
def cadastrar_equipamento(nome, quantidade):
    conn = conexao()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO equipamento (nome, quantidade_disponivel) VALUES (?, ?)", (nome, quantidade))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False
    finally:
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

def atualizar_equipamento(id_equipamento, nome, quantidade):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE equipamento SET nome = ? , quantidade_disponivel = ? WHERE id = ?", (nome, quantidade, id_equipamento))
    conn.commit()
    conn.close()  

def cadastrar_sala(nome, numero, andar, capacidade, observacoes, status):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sala (nome, numero, andar, capacidade, observacoes, status) VALUES (?, ?, ?, ?, ?, ?)", (nome, numero, andar, capacidade, observacoes, status))
    id_sala = cursor.lastrowid   # devolve o id da sala recem-criada (util p/ associar equipamentos)
    conn.commit()
    conn.close()
    return id_sala

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

# Melhoria feita por Dener em 17/06/2026
# Antes eu pedia "criado_em" como parametro e mandava na mao para o banco.
# Mas a coluna "criado_em" ja tem um DEFAULT (datetime('now','localtime')) la na criacao da tabela,
# entao o proprio banco preenche a data/hora sozinho.
# Tirei "criado_em" daqui para nao repetir e para nao correr o risco de gravar uma data errada.
def cadastrar_reserva(id_sala, id_cliente, data, hora_inicio, hora_fim, status):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reserva (id_sala, id_cliente, data, hora_inicio, hora_fim, status) VALUES (?, ?, ?, ?, ?, ?)", (id_sala, id_cliente, data, hora_inicio, hora_fim, status))
    conn.commit()
    conn.close()

# Melhoria feita por Dener em 17/06/2026
# Aqui eu arrumei o JOIN: antes ele ligava "reserva.id = sala.id" e "reserva.id = cliente.id",
# o que estava errado, porque o id da reserva nao tem relacao com o id da sala/cliente.
# O certo e ligar pelas chaves estrangeiras: reserva.id_sala -> sala.id e reserva.id_cliente -> cliente.id.
# Tambem coloquei "reserva.id" como primeira coluna do SELECT, para depois eu saber qual
# reserva editar ou cancelar na tela.
def db_listar_reservas():
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT reserva.id,
                          sala.nome,
                          cliente.nome,
                          reserva.data,
                          reserva.hora_inicio,
                          reserva.hora_fim,
                          reserva.status,
                          reserva.criado_em
                   FROM reserva
                   INNER JOIN sala    ON  reserva.id_sala = sala.id
                   INNER JOIN cliente ON  reserva.id_cliente = cliente.id
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

# Melhoria feita por Dener em 17/06/2026
# "criado_em" e a data em que a reserva foi CRIADA. Quando a gente edita uma reserva,
# essa data nao pode mudar (senao a gente perde o registro de quando ela nasceu).
# Por isso tirei "criado_em" do UPDATE: agora a edicao mexe so nos outros campos.
def db_atualizar_reserva(id_reserva, id_sala, id_cliente, data, hora_inicio, hora_fim, status):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE reserva SET id_sala = ?, id_cliente = ?, data = ?, hora_inicio = ?, hora_fim = ?, status = ? WHERE id = ?", (id_sala, id_cliente, data, hora_inicio, hora_fim, status, id_reserva))
    conn.commit()
    conn.close()

# Melhoria feita por Dener em 25/06/2026
# Cancela uma reserva (muda so o status para 'cancelada'). A reserva continua
# no historico, mas deixa de ocupar a sala (checar_conflito_reserva so olha 'ativa').
def cancelar_reserva(id_reserva):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE reserva SET status = 'cancelada' WHERE id = ?", (id_reserva,))
    conn.commit()
    conn.close()

# Melhoria feita por Dener em 17/06/2026
# A tabela sala_equipamento tem chave primaria (id_sala, id_equipamento), ou seja, o mesmo
# equipamento nao pode ser ligado duas vezes na mesma sala. Antes, tentar repetir quebrava o programa.
# Coloquei try/except: se a ligacao ja existir, devolve False; se criar certo, devolve True.
def cadastrar_sala_equipamento(id_sala, id_equipamento, quantidade=1):
    conn = conexao()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO sala_equipamento (id_sala, id_equipamento, quantidade) VALUES (?, ?, ?)",
                       (id_sala, id_equipamento, quantidade))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False
    finally:
        conn.close()

# Melhoria feita por Dener em 25/06/2026
# Cadastra a SALA e ja ASSOCIA os equipamentos escolhidos numa unica transacao.
# "equipamentos" e uma lista de tuplas (id_equipamento, quantidade).
# Se qualquer parte falhar, NADA e gravado (rollback) - assim nunca fica uma
# sala "pela metade", sem os equipamentos que o usuario pediu.
# Retorna o id da sala criada.
def cadastrar_sala_com_equipamentos(nome, numero, andar, capacidade, observacoes, status, equipamentos):
    conn = conexao()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO sala (nome, numero, andar, capacidade, observacoes, status) VALUES (?, ?, ?, ?, ?, ?)",
                       (nome, numero, andar, capacidade, observacoes, status))
        id_sala = cursor.lastrowid
        for id_equipamento, quantidade in equipamentos:
            cursor.execute("INSERT INTO sala_equipamento (id_sala, id_equipamento, quantidade) VALUES (?, ?, ?)",
                           (id_sala, id_equipamento, quantidade))
        conn.commit()
        return id_sala
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()

def db_listar_sala_equipamento():
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT sala.nome,
                          equipamento.nome,
                          sala_equipamento.quantidade
                   FROM sala_equipamento
                   INNER JOIN sala ON sala_equipamento.id_sala = sala.id
                   INNER JOIN equipamento ON sala_equipamento.id_equipamento = equipamento.id
                  """)
    dados = cursor.fetchall()
    conn.close()
    return dados

# Lista os equipamentos associados a UMA sala especifica (id, nome, quantidade).
def listar_equipamentos_da_sala(id_sala):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT equipamento.id,
                          equipamento.nome,
                          sala_equipamento.quantidade
                   FROM sala_equipamento
                   INNER JOIN equipamento ON sala_equipamento.id_equipamento = equipamento.id
                   WHERE sala_equipamento.id_sala = ?
                   ORDER BY equipamento.nome
                  """, (id_sala,))
    dados = cursor.fetchall()
    conn.close()
    return dados

#Manipulação para o sistema do projeto
#Kael: Adicionando a manipulação para atualizar o status da sala na hora de reservar 
#e recuperação da nova senha
def atualizar_status_sala(id_sala, status):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE sala SET status = ? WHERE id = ?", (status, id_sala))
    conn.commit()
    conn.close()  

def recuperar_senha(id_senha, senha_hash):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE administrador SET senha_hash = ? WHERE id = ?", (senha_hash, id_senha))
    conn.commit()
    conn.close()  

#Melhoria feita por Fernando em 24/06/2026
#Esta função verifica se há conflito de horários para uma reserva em uma sala específica.
#Ela faz uma consulta ao banco de dados para contar quantas reservas ativas existem para a mesma sala e data,
#e verifica se os horários de início e fim da nova reserva se sobrepõem com alguma das reservas existentes.
#Se houver conflito, a função retorna True; caso contrário, retorna False.
def checar_conflito_reserva(id_sala, data, hora_inicio, hora_fim):
    conn = conexao()
    cursor = conn.cursor()
    # Verifica se há sobreposição de horários para a mesma sala e data em reservas 'ativa'
    cursor.execute("""
        SELECT COUNT(*) FROM reserva 
        WHERE id_sala = ? AND data = ? AND status = 'ativa'
        AND ((hora_inicio < ? AND hora_fim > ?) OR (hora_inicio >= ? AND hora_inicio < ?))
    """, (id_sala, data, hora_fim, hora_inicio, hora_inicio, hora_fim))
    
    conflitos = cursor.fetchone()[0]
    conn.close()
    return conflitos > 0

    




