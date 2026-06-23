# ============================================================
# TELA DE BACKUP / CONFIGURACOES  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Cartao central com as duas acoes principais (exportar/importar).
# ============================================================

import tkinter as tk
from tkinter import messagebox
import ui


def montar_backup(container, navegar):
    ui.limpar(container)
    ui.barra_topo(container, "Backup e Configuracoes",
                  lambda: navegar("dashboard"))

    cartao = ui.card(container)
    cartao.place(relx=0.5, rely=0.5, anchor="center")
    interno = tk.Frame(cartao, bg=ui.COR_CARD)
    interno.pack(padx=44, pady=36)

    lg = ui.icone("backup", 44, ui.COR_PRIMARIA)
    li = tk.Label(interno, image=lg, bg=ui.COR_CARD)
    li.image = lg
    li.pack()
    ui.lbl(interno, "Copia de seguranca", fonte=ui.F_H2).pack(pady=(8, 2))
    ui.lbl(interno, "Salve ou restaure o banco de dados do sistema.",
           fonte=ui.F_PEQ, fg=ui.COR_TEXTO_FRACO).pack(pady=(0, 18))

    ui.botao(interno, "Exportar copia do banco",
             lambda: messagebox.showinfo("A fazer", "Exportar sera feito depois."),
             icone_nome="backup").pack(fill="x", pady=6)
    ui.botao(interno, "Importar banco de outro PC",
             lambda: messagebox.showinfo("A fazer", "Importar sera feito depois."),
             variante="neutro", icone_nome="config").pack(fill="x", pady=6)
