# ============================================================
# TELA DE BACKUP / CONFIGURACOES  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Cartao central com as duas acoes principais (exportar/importar).
#
# Backup = uma copia de seguranca do banco de dados.
# Exportar = salva uma copia atual do banco em outro local.
# Importar = substitui o banco atual por uma copia escolhida.
# ============================================================

import tkinter as tk
from tkinter import messagebox, filedialog  # dialogo para escolher o local do backup
import shutil  # faz a copia do banco de dados para outro local
import ui


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
            messagebox.showinfo("Sucesso", "Backup exportado com sucesso.")

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
                messagebox.showinfo("Sucesso", "Banco importado com sucesso.")

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            f"Não foi possivel importar o backup.\n\n{erro}"
        )


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
             exportar_backup,
             icone_nome="backup").pack(fill="x", pady=6)
    ui.botao(interno, "Importar banco de outro PC",
             importar_backup,
             variante="neutro", icone_nome="config").pack(fill="x", pady=6)
