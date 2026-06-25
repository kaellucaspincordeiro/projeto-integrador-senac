# ============================================================
# TELA DE CADASTRO DE CLIENTE  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Cartao central com os dados do cliente. Ja salva no banco.
# Modificações feitas por Dener (25/06/2026)
#   - Validacoes de verdade: CPF (Fisica) e CNPJ (Juridica) com digitos
#     verificadores, e-mail e telefone (usando o modulo validacoes.py).
#   - O documento e o telefone sao gravados ja formatados (com mascara), o que
#     tambem evita duplicar o mesmo CPF/CNPJ digitado de jeitos diferentes.
# ============================================================

import tkinter as tk
from tkinter import messagebox
import banco_dados as bd
import validacoes as val
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
    tk.Radiobutton(linha_tipo, text="Física (CPF)", variable=tipo, value="F",
                   bg=ui.COR_CARD, fg=ui.COR_TEXTO, font=ui.F_TEXTO,
                   activebackground=ui.COR_CARD, selectcolor=ui.COR_PRIM_CLARA).pack(side="left")
    tk.Radiobutton(linha_tipo, text="Jurídica (CNPJ)", variable=tipo, value="J",
                   bg=ui.COR_CARD, fg=ui.COR_TEXTO, font=ui.F_TEXTO,
                   activebackground=ui.COR_CARD, selectcolor=ui.COR_PRIM_CLARA).pack(side="left", padx=16)

    entrada_nome = ui.campo(interno, "NOME")
    entrada_telefone = ui.campo(interno, "TELEFONE")
    entrada_email = ui.campo(interno, "E-MAIL")
    entrada_cpf_cnpj = ui.campo(interno, "CPF / CNPJ")

    def salvar_cliente():
        t = tipo.get()
        nome = entrada_nome.get().strip()
        telefone = entrada_telefone.get().strip()
        email = entrada_email.get().strip()
        documento = entrada_cpf_cnpj.get().strip()

        # Nome obrigatorio
        if nome == "":
            messagebox.showwarning("Atenção", "Informe o nome do cliente.")
            return

        # CPF/CNPJ obrigatorio e VALIDO conforme o tipo escolhido
        if documento == "":
            messagebox.showwarning("Atenção", "Informe o CPF (Física) ou o CNPJ (Jurídica).")
            return
        if t == "F":
            if not val.validar_cpf(documento):
                messagebox.showwarning("CPF inválido",
                    "Digite um CPF válido (11 dígitos com os dígitos verificadores corretos).")
                return
            documento = val.formatar_cpf(documento)
        else:
            if not val.validar_cnpj(documento):
                messagebox.showwarning("CNPJ inválido",
                    "Digite um CNPJ válido (14 dígitos com os dígitos verificadores corretos).")
                return
            documento = val.formatar_cnpj(documento)

        # Telefone e e-mail sao opcionais; se preenchidos, precisam ser validos
        if telefone:
            if not val.validar_telefone(telefone):
                messagebox.showwarning("Telefone inválido",
                    "Digite um telefone com DDD (10 dígitos para fixo ou 11 para celular).")
                return
            telefone = val.formatar_telefone(telefone)
        if email and not val.validar_email(email):
            messagebox.showwarning("E-mail inválido",
                "Digite um e-mail válido (exemplo: nome@dominio.com).")
            return

        # Tudo certo: grava no banco (documento e telefone ja formatados)
        deu_certo = bd.cadastrar_cliente(t, nome, telefone, email, documento)
        if deu_certo:
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            navegar("dashboard")
        else:
            messagebox.showerror("Erro", "Já existe um cliente com esse CPF/CNPJ.")

    ui.botao(interno, "Salvar cliente", salvar_cliente,
             icone_nome="disponivel").pack(fill="x", pady=(20, 0))
