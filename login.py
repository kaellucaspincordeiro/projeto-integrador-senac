# ============================================================
# TELA DE LOGIN
# Tela criada por Dener em 17/06/2026
# ------------------------------------------------------------
# Esta e a primeira tela que aparece quando o programa abre.
# Aqui o administrador digita o e-mail e a senha para entrar.
#
# Como funciona o "navegar":
#   - "navegar" e uma funcao que mora la no main.py.
#   - Quando a gente chama navegar("dashboard"), o programa troca
#     esta tela pela tela do dashboard. E so dizer o nome da tela.
# ============================================================

import tkinter as tk
from tkinter import messagebox


def montar_login(container, navegar):
    # Antes de desenhar a tela, apagamos tudo que estava no container.
    # (assim nao fica sobrando nada da tela anterior na frente)
    for widget in container.winfo_children():
        widget.destroy()

    # Um "Frame" e como uma caixa onde a gente organiza os campos.
    # O place(...) com anchor="center" deixa a caixa no meio da tela.
    quadro = tk.Frame(container)
    quadro.place(relx=0.5, rely=0.5, anchor="center")

    # Titulo do sistema
    tk.Label(quadro, text="ShareSpace", font=("Arial", 28, "bold")).pack(pady=(0, 5))
    tk.Label(quadro, text="Gestao de Salas de Reuniao", font=("Arial", 12)).pack(pady=(0, 20))

    # Campo do e-mail
    tk.Label(quadro, text="E-mail:", font=("Arial", 12)).pack(anchor="w")
    entrada_email = tk.Entry(quadro, width=35)
    entrada_email.pack(pady=(0, 10))

    # Campo da senha. O show="*" esconde a senha com bolinhas.
    tk.Label(quadro, text="Senha:", font=("Arial", 12)).pack(anchor="w")
    entrada_senha = tk.Entry(quadro, width=35, show="*")
    entrada_senha.pack(pady=(0, 15))

    # Esta funcao roda quando clicamos no botao ENTRAR.
    def tentar_entrar():
        email = entrada_email.get()   # .get() pega o que foi digitado
        senha = entrada_senha.get()

        # POR ENQUANTO so checamos se os campos estao preenchidos.
        # MAIS PARA FRENTE: aqui vamos conferir o e-mail e a senha no banco de dados.
        if email == "" or senha == "":
            messagebox.showwarning("Atencao", "Preencha o e-mail e a senha.")
            return

        navegar("dashboard")  # deu certo -> vai para a tela inicial

    # Botao ENTRAR (o command diz qual funcao roda ao clicar)
    tk.Button(quadro, text="ENTRAR", width=20, bg="#1f4fc4", fg="white",
              command=tentar_entrar).pack(pady=(0, 10))

    # Texto "Esqueci minha senha" -> abre a tela de recuperar senha.
    # Usamos lambda para "guardar" a acao de navegar so quando clicar.
    tk.Button(quadro, text="Esqueci minha senha", borderwidth=0, fg="#1f4fc4",
              command=lambda: navegar("recuperar_senha")).pack()
