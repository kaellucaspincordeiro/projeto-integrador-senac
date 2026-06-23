# ============================================================
# TELA DE RECUPERAR SENHA  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Cartao centralizado com a pergunta de seguranca e a nova senha.
# Modificado por Fernando (23/06/2026) - Ajustes de ortografia e layout.
# ============================================================

import tkinter as tk
from tkinter import messagebox
import ui


def montar_recuperar_senha(container, navegar):
    ui.limpar(container)

    cartao = ui.card(container)
    cartao.place(relx=0.5, rely=0.5, anchor="center")
    interno = tk.Frame(cartao, bg=ui.COR_CARD)
    interno.pack(padx=48, pady=42)

    lg = ui.icone("senha", 44, ui.COR_PRIMARIA)
    cab = tk.Label(interno, image=lg, bg=ui.COR_CARD)
    cab.image = lg
    cab.pack()
    ui.lbl(interno, "Recuperar Senha", fonte=ui.F_H1).pack(pady=(10, 2))
    ui.lbl(interno, "Responda à pergunta de segurança para criar uma nova senha.",
           fonte=ui.F_PEQ, fg=ui.COR_TEXTO_FRACO).pack(pady=(0, 12))

    ui.lbl(interno, "Pergunta: Nome do seu primeiro animal?",
           fonte=ui.F_LABEL, fg=ui.COR_TEXTO_FRACO).pack(anchor="w", pady=(6, 0))
    entrada_resposta = ui.campo(interno, "RESPOSTA")
    entrada_nova_senha = ui.campo(interno, "NOVA SENHA", show="*")

    def salvar_nova_senha():
        messagebox.showinfo("Tudo certo", "Aqui vamos salvar a nova senha (a fazer).")
        navegar("login")

    ui.botao(interno, "Salvar nova senha", salvar_nova_senha,
             icone_nome="disponivel").pack(fill="x", pady=(22, 10))
    ui.botao_link(interno, "< Voltar para o login",
                  lambda: navegar("login")).pack()
