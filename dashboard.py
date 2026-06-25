# ============================================================
# TELA DASHBOARD  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Painel principal: cabecalho com a marca, cartoes de numeros
# (resumo) e uma grade de cartoes clicaveis (o menu).
# Tudo se ajusta quando a janela cresce (grid + weight).
# Modificado por Fernando (23/06/2026) - Ajustes de ortografia e layout.
# Modificado por Fernando (25/06/2026) - Adicionado o cartao de agendamento.
# ============================================================

import tkinter as tk
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
    corpo.pack(fill="both", expand=True, padx=28, pady=20)

    ui.lbl(corpo, "Visão geral", fonte=ui.F_H2, bg=ui.COR_FUNDO).pack(anchor="w")

    # ---- Cartoes de numeros (resumo) ----
    stats = tk.Frame(corpo, bg=ui.COR_FUNDO)
    stats.pack(fill="x", pady=(10, 22))
    indicadores = [
        ("ocupacao",   ui.COR_PRIMARIA, "62%", "Ocupação geral"),
        ("disponivel", ui.COR_SUCESSO,  "38%", "Salas disponíveis"),
        ("manutencao", ui.COR_AVISO,    "1",   "Salas em manutenção"),
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
