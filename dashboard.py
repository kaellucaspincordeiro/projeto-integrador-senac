# ============================================================
# TELA DASHBOARD  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Painel principal: cabecalho com a marca, cartoes de numeros
# (resumo) e uma grade de cartoes clicaveis (o menu).
# Tudo se ajusta quando a janela cresce (grid + weight).
# Modificado por Fernando (23/06/2026) - Ajustes de ortografia e layout.
# Modificado por Fernando (25/06/2026) - Adicionado o cartao de agendamento.
# Modificado por Dener (25/06/2026) - Os cartoes de numeros agora mostram dados
#   REAIS do banco (antes eram valores fixos no codigo).
# ============================================================

import tkinter as tk
from datetime import date
import banco_dados as bd
import ui


def montar_dashboard(container, navegar):
    ui.limpar(container)

    # ---- Cabecalho (barra branca no topo) ----
    cab = tk.Frame(container, bg=ui.COR_CARD,
                   highlightbackground=ui.COR_BORDA, highlightthickness=1)
    cab.pack(fill="x")
    cabint = tk.Frame(cab, bg=ui.COR_CARD)
    cabint.pack(fill="x", padx=28, pady=14)

    lg = ui.logo(34)
    li = tk.Label(cabint, image=lg, bg=ui.COR_CARD)
    li.image = lg
    li.pack(side="left")
    ui.lbl(cabint, "ShareSpace", fonte=ui.F_LOGO).pack(side="left", padx=10)
    ui.botao(cabint, "Sair", lambda: navegar("login"),
             variante="neutro", icone_nome="sair").pack(side="right")

    # ---- Corpo ----
    corpo = tk.Frame(container, bg=ui.COR_FUNDO)
    corpo.pack(fill="both", expand=True, padx=28, pady=(14, 12))

    ui.lbl(corpo, "Visão geral", fonte=ui.F_H2, bg=ui.COR_FUNDO).pack(anchor="w")

    # ---- Cartoes de numeros (resumo) - DADOS REAIS do banco ----
    salas = bd.listar_salas()          # (id, nome, numero, andar, capac, obs, status)
    reservas = bd.db_listar_reservas() # (id, sala, cliente, data, inicio, fim, status, criado_em)

    total_salas = len(salas)
    disponiveis = sum(1 for s in salas if s[6] == "disponivel")
    em_manutencao = sum(1 for s in salas if s[6] == "manutencao")
    reservas_ativas = sum(1 for r in reservas if r[6] == "ativa")

    # Ocupacao de hoje = salas com reserva ativa hoje / total de salas
    hoje = date.today().strftime("%Y-%m-%d")
    ocupadas_hoje = len({r[1] for r in reservas if r[6] == "ativa" and r[3] == hoje})
    ocupacao = round(ocupadas_hoje / total_salas * 100) if total_salas else 0

    stats = tk.Frame(corpo, bg=ui.COR_FUNDO)
    stats.pack(fill="x", pady=(8, 14))
    indicadores = [
        ("ocupacao",    ui.COR_PRIMARIA, f"{ocupacao}%",         "Ocupação hoje"),
        ("disponivel",  ui.COR_SUCESSO,  str(disponiveis),       "Salas disponíveis"),
        ("manutencao",  ui.COR_AVISO,    str(em_manutencao),     "Em manutenção"),
        ("agendamento", ui.COR_PRIMARIA, str(reservas_ativas),   "Reservas ativas"),
    ]
    for i, (ic, cor, val, desc) in enumerate(indicadores):
        c = ui.card_estatistica(stats, ic, cor, val, desc)
        c.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 14, 0))
        stats.columnconfigure(i, weight=1)

    # ---- Grade de cartoes do menu ----
    ui.lbl(corpo, "Ações", fonte=ui.F_H2, bg=ui.COR_FUNDO).pack(anchor="w", pady=(4, 8))
    menu = tk.Frame(corpo, bg=ui.COR_FUNDO)
    menu.pack(fill="both", expand=True)

    cartoes = [
        ("agendamento",  "Novo Agendamento",      "agendamento"), 
        ("busca",        "Buscar Salas",          "busca"),
        ("equipamento",  "Cadastrar Equipamento", "cadastro_equipamento"),
        ("sala",         "Cadastrar Sala",        "cadastro_sala"),
        ("cliente",      "Cadastrar Cliente",     "cadastro_cliente"),
        ("historico",    "Histórico de Reservas", "historico"),
        ("backup",       "Backup / Config.",      "backup"),
    ]
    colunas = 3
    for idx, (ic, titulo, tela) in enumerate(cartoes):
        linha, col = divmod(idx, colunas)
        c = ui.card_menu(menu, ic, titulo, lambda t=tela: navegar(t))
        c.grid(row=linha, column=col, sticky="nsew", padx=8, pady=8)
    for col in range(colunas):
        menu.columnconfigure(col, weight=1)
    for linha in range((len(cartoes) + colunas - 1) // colunas):
        menu.rowconfigure(linha, weight=1)
