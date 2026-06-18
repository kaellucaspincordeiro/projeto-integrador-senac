# ============================================================
# TELA DE BACKUP / CONFIGURACOES
# Tela criada por Dener em 17/06/2026
# ------------------------------------------------------------
# Backup = uma copia de seguranca do banco de dados.
# Aqui o administrador podera salvar uma copia e tambem trazer
# uma copia de outro computador.
#
# POR ENQUANTO os botoes so mostram um aviso. A parte de copiar
# o arquivo do banco vamos programar depois.
# ============================================================

import tkinter as tk
from tkinter import messagebox


def montar_backup(container, navegar):
    # limpa a tela anterior
    for widget in container.winfo_children():
        widget.destroy()

    tk.Button(container, text="< Voltar", bg="#1f4fc4", fg="white",
              command=lambda: navegar("dashboard")).pack(anchor="w", padx=10, pady=10)

    quadro = tk.Frame(container)
    quadro.place(relx=0.5, rely=0.4, anchor="center")

    tk.Label(quadro, text="Backup e Configuracoes", font=("Arial", 18, "bold")).pack(pady=(0, 20))

    # MAIS PARA FRENTE: este botao vai copiar o arquivo do banco para uma pasta de backup.
    tk.Button(quadro, text="Exportar copia do banco", width=30, height=2, bg="#1f4fc4", fg="white",
              command=lambda: messagebox.showinfo("A fazer", "Exportar sera feito depois.")).pack(pady=8)

    # MAIS PARA FRENTE: este botao vai trazer um banco de outro computador.
    tk.Button(quadro, text="Importar banco de outro PC", width=30, height=2, bg="#1f4fc4", fg="white",
              command=lambda: messagebox.showinfo("A fazer", "Importar sera feito depois.")).pack(pady=8)
