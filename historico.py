# ============================================================
# TELA DE HISTORICO DE RESERVAS
# Tela criada por Dener em 17/06/2026
# ------------------------------------------------------------
# Mostra, em forma de tabela, todas as reservas que existem.
# Os dados vem da funcao db_listar_reservas() do banco_dados.py
# (aquela em que a gente arrumou o JOIN!).
# ============================================================

import tkinter as tk
from tkinter import ttk
import banco_dados as bd


def montar_historico(container, navegar):
    # limpa a tela anterior
    for widget in container.winfo_children():
        widget.destroy()

    tk.Button(container, text="< Voltar", bg="#1f4fc4", fg="white",
              command=lambda: navegar("dashboard")).pack(anchor="w", padx=10, pady=10)

    tk.Label(container, text="Historico de Reservas", font=("Arial", 18, "bold")).pack(pady=(0, 10))

    # A "Treeview" do ttk e uma tabela com colunas.
    # Estas sao as colunas, na MESMA ordem que a funcao db_listar_reservas() devolve.
    colunas = ("id", "sala", "cliente", "data", "inicio", "fim", "status", "criado_em")
    tabela = ttk.Treeview(container, columns=colunas, show="headings", height=15)

    # Para cada coluna, escrevemos o titulo (o que aparece no topo) e a largura.
    for c in colunas:
        tabela.heading(c, text=c.capitalize())
        tabela.column(c, width=100)
    tabela.pack(fill="both", expand=True, padx=20, pady=10)

    # Buscamos as reservas no banco e colocamos cada uma como uma linha da tabela.
    reservas = bd.db_listar_reservas()
    for linha in reservas:
        # "values=linha" preenche as colunas com os valores daquela reserva.
        tabela.insert("", "end", values=linha)
