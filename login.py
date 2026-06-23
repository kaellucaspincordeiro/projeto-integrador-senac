# ============================================================
# TELA DE LOGIN  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Primeira tela do sistema. Visual de "cartao centralizado",
# que se mantem no meio em qualquer tamanho de janela.
# Modificado por Fernando (23/06/2026) - Ajustes de ortografia e layout.
# ============================================================

import tkinter as tk
from tkinter import messagebox
import ui


def montar_login(container, navegar):
    ui.limpar(container)

    # Cartao branco centralizado (place mantem no meio sempre)
    cartao = ui.card(container)
    cartao.place(relx=0.5, rely=0.5, anchor="center")
    interno = tk.Frame(cartao, bg=ui.COR_CARD)
    interno.pack(padx=48, pady=42)

    # Logo + nome do sistema
    lg = ui.logo(60)
    cab = tk.Label(interno, image=lg, bg=ui.COR_CARD)
    cab.image = lg
    cab.pack()
    ui.lbl(interno, "ShareSpace", fonte=ui.F_LOGO).pack(pady=(12, 0))
    ui.lbl(interno, "Gestão de Salas de Reunião",
           fonte=ui.F_TEXTO, fg=ui.COR_TEXTO_FRACO).pack(pady=(2, 20))

    # Campos
    entrada_email = ui.campo(interno, "E-MAIL")
    entrada_senha = ui.campo(interno, "SENHA", show="*")

    def tentar_entrar():
        email = entrada_email.get()
        senha = entrada_senha.get()
        if email == "" or senha == "":
            messagebox.showwarning("Atenção", "Preencha o e-mail e a senha.")
            entrada_email.delete(0, "end")
            entrada_senha.delete(0, "end")
            entrada_email.focus()
            return
        navegar("dashboard")

    ui.botao(interno, "ENTRAR", tentar_entrar).pack(fill="x", pady=(22, 10))
    ui.botao_link(interno, "Esqueci minha senha",
                  lambda: navegar("recuperar_senha")).pack()
