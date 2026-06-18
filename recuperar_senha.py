# ============================================================
# TELA DE RECUPERAR SENHA
# Tela criada por Dener em 17/06/2026
# ------------------------------------------------------------
# Serve para quando o administrador esquece a senha.
# A ideia: ele responde uma pergunta pessoal (que cadastrou antes)
# e, se acertar, pode criar uma senha nova.
# ============================================================

import tkinter as tk
from tkinter import messagebox


def montar_recuperar_senha(container, navegar):
    # limpa a tela anterior
    for widget in container.winfo_children():
        widget.destroy()

    quadro = tk.Frame(container)
    quadro.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(quadro, text="Recuperar Senha", font=("Arial", 20, "bold")).pack(pady=(0, 20))

    # A pergunta de seguranca vem do cadastro do administrador.
    # POR ENQUANTO deixei um texto de exemplo. MAIS PARA FRENTE vamos
    # buscar a pergunta certa no banco de dados.
    tk.Label(quadro, text="Pergunta: Nome do seu primeiro animal?",
             font=("Arial", 11)).pack(anchor="w", pady=(0, 5))
    entrada_resposta = tk.Entry(quadro, width=35)
    entrada_resposta.pack(pady=(0, 15))

    tk.Label(quadro, text="Nova senha:", font=("Arial", 11)).pack(anchor="w")
    entrada_nova_senha = tk.Entry(quadro, width=35, show="*")
    entrada_nova_senha.pack(pady=(0, 15))

    def salvar_nova_senha():
        # MAIS PARA FRENTE: aqui vamos conferir a resposta no banco
        # e, se estiver certa, salvar a nova senha do administrador.
        messagebox.showinfo("Tudo certo", "Aqui vamos salvar a nova senha (a fazer).")
        navegar("login")

    tk.Button(quadro, text="Salvar nova senha", width=20, bg="#1f4fc4", fg="white",
              command=salvar_nova_senha).pack(pady=(0, 10))

    tk.Button(quadro, text="< Voltar para o login", borderwidth=0, fg="#1f4fc4",
              command=lambda: navegar("login")).pack()
