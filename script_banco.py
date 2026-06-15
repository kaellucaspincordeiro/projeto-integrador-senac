administrador = """
                CREATE TABLE IF NOT EXISTS administrador (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    senha_hash TEXT NOT NULL,
                    pergunta_seguranca TEXT NOT NULL,
                    resposta_seguranca_hash TEXT NOT NULL
                )
                """

equipamento = """
              CREATE TABLE IF NOT EXISTS equipamento (
                  id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  nome TEXT NOT NULL UNIQUE
              )
              """

sala = """
       CREATE TABLE IF NOT EXISTS sala (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           nome TEXT NOT NULL,
           numero TEXT NOT NULL,
           andar INTEGER NOT NULL CHECK (andar BETWEEN 1 AND 15),
           capacidade INTEGER NOT NULL CHECK (capacidade > 0),
           observacoes TEXT,
           status TEXT NOT NULL DEFAULT 'ativa'
                  CHECK (status IN ('ativa', 'manutencao'))
       )
       """

cliente = """
          CREATE TABLE IF NOT EXISTS cliente (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              tipo TEXT NOT NULL CHECK (tipo IN ('F', 'J')),
              nome TEXT NOT NULL,
              telefone TEXT,
              email TEXT,
              cpf_cnpj TEXT NOT NULL UNIQUE
          )
          """

sala_equipamento = """
                   CREATE TABLE IF NOT EXISTS sala_equipamento (
                        id_sala INTEGER NOT NULL,
                        id_equipamento INTEGER NOT NULL,
                        PRIMARY KEY (sala_id, equipamento_id),
                        CONSTRAINT fk_sala FOREIGN KEY (id_sala) REFERENCES sala (id) ON DELETE CASCADE,
                        CONSTRAINT fk_equipamento FOREIGN KEY (id_equipamento) REFERENCES equipamento (id) ON DELETE CASCADE
                   )
                   """

reserva = """
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
              CONSTRAINT fk_reserva_cliente FOREIGN KEY (id_cliente) REFERENCES cliente (id)    
          )
          """

busca = """
        CREATE INDEX idx_reserva_sala_data ON reserva (id_sala, data, status);
        """

