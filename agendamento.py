# ============================================================
# TELA DE AGENDAMENTO  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Cartao central com os campos da reserva (sala, cliente, data,
# horarios). As regras de negocio ficam para a proxima etapa.
# ============================================================

import tkinter as tk
from tkinter import messagebox
import banco_dados as bd
import ui


def montar_agendamento(container, navegar):
    ui.limpar(container)
    corpo = ui.barra_topo(container, "Novo Agendamento", lambda: navegar("dashboard"))

    cartao = ui.card(corpo)
    cartao.place(relx=0.5, rely=0.45, anchor="center")
    interno = tk.Frame(cartao, bg=ui.COR_CARD)
    interno.pack(padx=44, pady=34)

    ui.lbl(interno, "Dados da reserva", fonte=ui.F_H2).pack(anchor="w", pady=(0, 6))

    salas = bd.listar_salas()
    nomes_salas = [s[1] for s in salas]
    caixa_sala = ui.campo(interno, "SALA", valores=nomes_salas)

    clientes = bd.listar_clientes()
    nomes_clientes = [c[2] for c in clientes]
    caixa_cliente = ui.campo(interno, "CLIENTE", valores=nomes_clientes)

    entrada_data = ui.campo(interno, "DATA (AAAA-MM-DD)")
    entrada_inicio = ui.campo(interno, "HORA INICIO (HH:MM)")
    entrada_fim = ui.campo(interno, "HORA FIM (HH:MM)")

    ui.lbl(interno, "minimo 30min, maximo 4h, seg a sex das 08h as 18h",
           fonte=ui.F_PEQ, fg=ui.COR_TEXTO_FRACO).pack(anchor="w", pady=(8, 0))

    def confirmar():
        messagebox.showinfo("A fazer",
                            "A logica de salvar a reserva sera feita na proxima etapa.")

    ui.botao(interno, "Confirmar reserva", confirmar,
             icone_nome="disponivel").pack(fill="x", pady=(20, 0))
