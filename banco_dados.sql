-- ============================================================
-- Sistema de Gestão de Salas de Reunião - Projeto Integrador 2026
-- Equipe: Dener, Kael e Fernando
-- Banco de dados: SQLite
-- Script de criação das tabelas
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- Administrador (usuário único do sistema)
-- ------------------------------------------------------------
CREATE TABLE administrador (
    id                       INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                     TEXT    NOT NULL,
    email                    TEXT    NOT NULL UNIQUE,
    senha_hash               TEXT    NOT NULL,
    pergunta_seguranca       TEXT    NOT NULL,
    resposta_seguranca_hash  TEXT    NOT NULL
);

-- ------------------------------------------------------------
-- Sala
-- ------------------------------------------------------------
CREATE TABLE sala (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT    NOT NULL,
    numero       TEXT    NOT NULL,
    andar        INTEGER NOT NULL CHECK (andar BETWEEN 1 AND 15),
    capacidade   INTEGER NOT NULL CHECK (capacidade > 0),
    observacoes  TEXT,
    status       TEXT    NOT NULL DEFAULT 'ativa'
                 CHECK (status IN ('ativa', 'manutencao'))
);

-- ------------------------------------------------------------
-- Equipamento (catálogo de recursos)
-- ------------------------------------------------------------
CREATE TABLE equipamento (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome  TEXT    NOT NULL UNIQUE
);

-- ------------------------------------------------------------
-- Relação N:N entre sala e equipamento
-- (equipamentos são fixos da sala, definidos no cadastro da sala)
-- ------------------------------------------------------------
CREATE TABLE sala_equipamento (
    sala_id         INTEGER NOT NULL,
    equipamento_id  INTEGER NOT NULL,
    PRIMARY KEY (sala_id, equipamento_id),
    FOREIGN KEY (sala_id)        REFERENCES sala(id)        ON DELETE CASCADE,
    FOREIGN KEY (equipamento_id) REFERENCES equipamento(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Cliente (pessoa física ou jurídica)
-- ------------------------------------------------------------
CREATE TABLE cliente (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo       TEXT NOT NULL CHECK (tipo IN ('F', 'J')),  -- F = física, J = jurídica
    nome       TEXT NOT NULL,
    telefone   TEXT,
    email      TEXT,
    cpf_cnpj   TEXT NOT NULL UNIQUE  -- validado no aplicativo (dígitos verificadores)
);

-- ------------------------------------------------------------
-- Reserva / Agendamento
-- ------------------------------------------------------------
CREATE TABLE reserva (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    sala_id      INTEGER NOT NULL,
    cliente_id   INTEGER NOT NULL,
    data         TEXT    NOT NULL,  -- formato AAAA-MM-DD
    hora_inicio  TEXT    NOT NULL,  -- formato HH:MM
    hora_fim     TEXT    NOT NULL,  -- formato HH:MM
    status       TEXT    NOT NULL DEFAULT 'ativa'
                 CHECK (status IN ('ativa', 'cancelada')),
    criado_em    TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (sala_id)    REFERENCES sala(id),
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

-- Índice para acelerar a busca de disponibilidade por sala/data
CREATE INDEX idx_reserva_sala_data ON reserva (sala_id, data, status);

-- ------------------------------------------------------------
-- Observações de regras tratadas no aplicativo (Python):
--  * RN1 - conflito de horário (sobreposição) na mesma sala.
--  * RN5 - duração entre 30 min e 4 horas.
--  * RN6 - apenas seg-sex, 08:00-18:00.
--  * RN7 - não permitir data/horário passados.
--  * RN2 - validação dos dígitos de CPF/CNPJ.
-- ------------------------------------------------------------

-- ============================================================
-- Dados de exemplo (opcional, para testes)
-- ============================================================
INSERT INTO administrador (nome, email, senha_hash, pergunta_seguranca, resposta_seguranca_hash)
VALUES ('Administrador', 'admin@predio.com', 'HASH_DA_SENHA', 'Nome do seu primeiro animal?', 'HASH_DA_RESPOSTA');

INSERT INTO equipamento (nome) VALUES ('Projetor'), ('TV'), ('Videoconferência'), ('Lousa'), ('Ar-condicionado');

INSERT INTO sala (nome, numero, andar, capacidade, observacoes, status)
VALUES ('Sala Alfa', '101', 1, 8, 'Sala com vista para a rua', 'ativa'),
       ('Sala Beta', '502', 5, 20, 'Sala grande para treinamentos', 'ativa'),
       ('Sala Gama', '1503', 15, 4, 'Sala reservada para diretoria', 'manutencao');

INSERT INTO sala_equipamento (sala_id, equipamento_id) VALUES (1,1),(1,4),(2,2),(2,3),(2,5);

INSERT INTO cliente (tipo, nome, telefone, email, cpf_cnpj)
VALUES ('F', 'João da Silva', '(11) 99999-0000', 'joao@email.com', '12345678909'),
       ('J', 'Empresa XPTO Ltda', '(11) 3333-0000', 'contato@xpto.com', '12345678000199');

INSERT INTO reserva (sala_id, cliente_id, data, hora_inicio, hora_fim, status)
VALUES (1, 1, '2026-06-15', '09:00', '10:30', 'ativa'),
       (2, 2, '2026-06-15', '14:00', '17:00', 'ativa');
