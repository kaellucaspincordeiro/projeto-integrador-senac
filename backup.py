# ============================================================
# TELA DE BACKUP / CONFIGURACOES
# Tela criada por Dener em 17/06/2026
# Tela modificada por Fernando em 23/06/2026
# ------------------------------------------------------------
# Backup = uma copia de seguranca do banco de dados.
# Aqui o administrador podera salvar a copia e tambem trazer
# uma copia de outro computador.
#
# Exportar = salva uma copia atual do banco em outro local.
# Importar = substitui o banco atual por uma copia escolhida.
# ============================================================

import tkinter as tk
from tkinter import messagebox, filedialog # faz a interface grafica/dialogo para escolher o local do backup
import shutil # faz a copia do banco de dados para outro local


# ------------------------------------------------------------
# Exporta uma copia do banco para o local escolhido.
# ------------------------------------------------------------
def exportar_backup():
    try:
        destino = filedialog.asksaveasfilename(
            title="Salvar backup",
            defaultextension=".db",
            filetypes=[("Banco de Dados", "*.db")]
        )

        if destino:
            shutil.copy2("salas_reunioes.db", destino)

            messagebox.showinfo(
                "Sucesso",
                "Backup exportado com sucesso."
            )

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            f"Não foi possivel exportar o backup.\n\n{erro}"
        )


# ------------------------------------------------------------
# Importa uma copia de outro computador.
# O banco atual sera substituido.
# ------------------------------------------------------------
def importar_backup():
    try:
        origem = filedialog.askopenfilename(
            title="Selecionar backup",
            filetypes=[("Banco de Dados", "*.db")]
        )

        if origem:
            resposta = messagebox.askyesno(
                "Confirmação",
                "O banco atual será substituído.\n\nDeseja continuar?"
            )

            if resposta:
                shutil.copy2(origem, "salas_reunioes.db")

                messagebox.showinfo(
                    "Sucesso",
                    "Banco importado com sucesso."
                )

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            f"Não foi possivel importar o backup.\n\n{erro}"
        )


def montar_backup(container, navegar):
    # limpa a tela anterior
    for widget in container.winfo_children():
        widget.destroy()

    tk.Button(
        container,
        text="< Voltar",
        bg="#1f4fc4",
        fg="white",
        command=lambda: navegar("dashboard")
    ).pack(anchor="w", padx=10, pady=10)

    quadro = tk.Frame(container)
    quadro.place(relx=0.5, rely=0.4, anchor="center")

    tk.Label(
        quadro,
        text="Backup e Configurações",
        font=("Arial", 18, "bold")
    ).pack(pady=(0, 20))

    # Exporta uma copia do banco para outro local.
    tk.Button(
        quadro,
        text="Exportar cópia do banco",
        width=30,
        height=2,
        bg="#1f4fc4",
        fg="white",
        command=exportar_backup
    ).pack(pady=8)

    # Importa um banco vindo de outro computador.
    tk.Button(
        quadro,
        text="Importar banco de outro PC",
        width=30,
        height=2,
        bg="#1f4fc4",
        fg="white",
        command=importar_backup
    ).pack(pady=8)