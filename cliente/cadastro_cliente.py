# ============================================================
# TELA DE CADASTRO DE CLIENTE  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Cartao central com os dados do cliente. Ja salva no banco.
# ============================================================

import tkinter as tk
from tkinter import messagebox
import banco_dados as bd
import ui


def montar_cadastro_cliente(container, navegar):
    ui.limpar(container)
    corpo = ui.barra_topo(container, "Cadastro de Cliente", lambda: navegar("dashboard"))

    cartao = ui.card(corpo)
    cartao.place(relx=0.5, rely=0.45, anchor="center")
    interno = tk.Frame(cartao, bg=ui.COR_CARD)
    interno.pack(padx=44, pady=34)

    # Tipo: Fisica ou Juridica
    tipo = tk.StringVar(value="F")
    ui.lbl(interno, "TIPO", fonte=ui.F_LABEL, fg=ui.COR_TEXTO_FRACO).pack(anchor="w")
    linha_tipo = tk.Frame(interno, bg=ui.COR_CARD)
    linha_tipo.pack(anchor="w", pady=(2, 4))
    tk.Radiobutton(linha_tipo, text="Fisica (CPF)", variable=tipo, value="F",
                   bg=ui.COR_CARD, fg=ui.COR_TEXTO, font=ui.F_TEXTO,
                   activebackground=ui.COR_CARD, selectcolor=ui.COR_PRIM_CLARA).pack(side="left")
    tk.Radiobutton(linha_tipo, text="Juridica (CNPJ)", variable=tipo, value="J",
                   bg=ui.COR_CARD, fg=ui.COR_TEXTO, font=ui.F_TEXTO,
                   activebackground=ui.COR_CARD, selectcolor=ui.COR_PRIM_CLARA).pack(side="left", padx=16)

    entrada_nome = ui.campo(interno, "NOME")
    entrada_telefone = ui.campo(interno, "TELEFONE")
    entrada_email = ui.campo(interno, "E-MAIL")
    entrada_cpf_cnpj = ui.campo(interno, "CPF / CNPJ")

    def salvar_cliente():
        nome = entrada_nome.get()
        cpf_cnpj = entrada_cpf_cnpj.get()
        if nome == "" or cpf_cnpj == "":
            messagebox.showwarning("Atencao", "Preencha pelo menos o Nome e o CPF/CNPJ.")
            return
        deu_certo = bd.cadastrar_cliente(
            tipo.get(), nome, entrada_telefone.get(), entrada_email.get(), cpf_cnpj)
        if deu_certo:
            messagebox.showinfo("Sucesso", "Cliente cadastrado!")
            navegar("dashboard")
        else:
            messagebox.showerror("Erro", "Ja existe um cliente com esse CPF/CNPJ.")

    ui.botao(interno, "Salvar cliente", salvar_cliente,
             icone_nome="disponivel").pack(fill="x", pady=(20, 0))
