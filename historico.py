# ============================================================
# TELA DE HISTORICO DE RESERVAS  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Tabela estilizada (cabecalho azul + linhas zebra) que cresce
# junto com a janela.
# Modificado por Fernando (23/06/2026) - Ajustes de ortografia e layout.
# ============================================================

import tkinter as tk
from tkinter import ttk
import banco_dados as bd
import ui


def montar_historico(container, navegar):
    ui.limpar(container)
    corpo = ui.barra_topo(container, "Histórico de Reservas",
                          lambda: navegar("dashboard"))

    cartao = ui.card(corpo)
    cartao.pack(fill="both", expand=True)
    cartao.rowconfigure(0, weight=1)
    cartao.columnconfigure(0, weight=1)

    colunas = ("id", "sala", "cliente", "data", "início", "fim", "status", "criado_em")
    tabela = ttk.Treeview(cartao, columns=colunas, show="headings")
    larguras = {"id": 50, "sala": 150, "cliente": 160, "data": 100,
                "início": 80, "fim": 80, "status": 110, "criado_em": 150}
    for c in colunas:
        tabela.heading(c, text=c.replace("_", " ").capitalize())
        tabela.column(c, width=larguras.get(c, 100), anchor="center")

    scroll = ttk.Scrollbar(cartao, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)
    tabela.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
    scroll.grid(row=0, column=1, sticky="ns", pady=10, padx=(0, 10))

    ui.zebrar(tabela, bd.db_listar_reservas())
