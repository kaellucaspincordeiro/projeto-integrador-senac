# ============================================================
# TELA DE CADASTRO DE CLIENTE
# Tela criada por Dener em 17/06/2026
# ------------------------------------------------------------
# Aqui cadastramos a pessoa que vai reservar a sala.
# Pode ser pessoa Fisica (usa CPF) ou Juridica (usa CNPJ).
#
# Esta tela JA conversa com o banco de dados: quando clicamos em
# Salvar, ela chama a funcao bd.cadastrar_cliente(...).
# ============================================================

import tkinter as tk
from tkinter import messagebox
import banco_dados as bd


def montar_cadastro_cliente(container, navegar):
    # limpa a tela anterior
    for widget in container.winfo_children():
        widget.destroy()

    # Botao para voltar ao menu principal (dashboard), no topo
    tk.Button(container, text="< Voltar", bg="#1f4fc4", fg="white",
              command=lambda: navegar("dashboard")).pack(anchor="w", padx=10, pady=10)

    quadro = tk.Frame(container)
    quadro.pack(pady=10)

    tk.Label(quadro, text="Cadastro de Cliente", font=("Arial", 18, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(0, 15))

    # Tipo: Fisica ou Juridica.
    # "StringVar" e uma caixinha que guarda qual opcao foi marcada.
    tipo = tk.StringVar(value="F")  # comeca marcado como Fisica
    tk.Label(quadro, text="Tipo:", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
    quadro_tipo = tk.Frame(quadro)
    quadro_tipo.grid(row=1, column=1, sticky="w")
    tk.Radiobutton(quadro_tipo, text="Fisica (CPF)", variable=tipo, value="F").pack(side="left")
    tk.Radiobutton(quadro_tipo, text="Juridica (CNPJ)", variable=tipo, value="J").pack(side="left")

    # Campos de texto
    tk.Label(quadro, text="Nome:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
    entrada_nome = tk.Entry(quadro, width=35)
    entrada_nome.grid(row=2, column=1, pady=5)

    tk.Label(quadro, text="Telefone:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
    entrada_telefone = tk.Entry(quadro, width=35)
    entrada_telefone.grid(row=3, column=1, pady=5)

    tk.Label(quadro, text="E-mail:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
    entrada_email = tk.Entry(quadro, width=35)
    entrada_email.grid(row=4, column=1, pady=5)

    tk.Label(quadro, text="CPF / CNPJ:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", pady=5)
    entrada_cpf_cnpj = tk.Entry(quadro, width=35)
    entrada_cpf_cnpj.grid(row=5, column=1, pady=5)

    # Esta funcao roda quando clicamos em Salvar.
    def salvar_cliente():
        nome = entrada_nome.get()
        cpf_cnpj = entrada_cpf_cnpj.get()

        # Checagem simples: nome e documento sao obrigatorios.
        # MAIS PARA FRENTE: aqui tambem vamos validar os digitos do CPF/CNPJ (regra RN2).
        if nome == "" or cpf_cnpj == "":
            messagebox.showwarning("Atencao", "Preencha pelo menos o Nome e o CPF/CNPJ.")
            return

        # Chamamos a funcao do banco de dados (esta no banco_dados.py).
        # Ela devolve True se cadastrou e False se o CPF/CNPJ ja existia.
        deu_certo = bd.cadastrar_cliente(
            tipo.get(), nome, entrada_telefone.get(), entrada_email.get(), cpf_cnpj)

        if deu_certo:
            messagebox.showinfo("Sucesso", "Cliente cadastrado!")
            navegar("dashboard")
        else:
            messagebox.showerror("Erro", "Ja existe um cliente com esse CPF/CNPJ.")

    tk.Button(quadro, text="Salvar", width=20, bg="#1f4fc4", fg="white",
              command=salvar_cliente).grid(row=6, column=0, columnspan=2, pady=20)
