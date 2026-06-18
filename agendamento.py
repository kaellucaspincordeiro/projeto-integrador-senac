# ============================================================
# TELA DE AGENDAMENTO (criar uma reserva)
# Tela criada por Dener em 17/06/2026
# ------------------------------------------------------------
# Aqui escolhemos a sala, o cliente, a data e o horario da reserva.
#
# As REGRAS (nao deixar horario repetido, reserva de 30min a 4h,
# so de segunda a sexta das 08h as 18h, sem data no passado)
# vamos programar na proxima etapa.
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import banco_dados as bd


def montar_agendamento(container, navegar):
    # limpa a tela anterior
    for widget in container.winfo_children():
        widget.destroy()

    tk.Button(container, text="< Voltar", bg="#1f4fc4", fg="white",
              command=lambda: navegar("dashboard")).pack(anchor="w", padx=10, pady=10)

    quadro = tk.Frame(container)
    quadro.pack(pady=10)

    tk.Label(quadro, text="Novo Agendamento", font=("Arial", 18, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(0, 15))

    # ---- Caixa de escolha da SALA ----
    # listar_salas() devolve uma lista de salas vinda do banco.
    # Cada sala e uma "tupla": (id, nome, numero, andar, ...).
    # Pegamos o nome de cada uma (posicao 1) para mostrar na caixinha.
    tk.Label(quadro, text="Sala:").grid(row=1, column=0, sticky="w", pady=5)
    salas = bd.listar_salas()
    nomes_salas = [s[1] for s in salas]   # s[1] = nome da sala
    caixa_sala = ttk.Combobox(quadro, values=nomes_salas, width=32)
    caixa_sala.grid(row=1, column=1, pady=5)

    # ---- Caixa de escolha do CLIENTE ----
    # Cada cliente e: (id, tipo, nome, telefone, ...). O nome esta na posicao 2.
    tk.Label(quadro, text="Cliente:").grid(row=2, column=0, sticky="w", pady=5)
    clientes = bd.listar_clientes()
    nomes_clientes = [c[2] for c in clientes]   # c[2] = nome do cliente
    caixa_cliente = ttk.Combobox(quadro, values=nomes_clientes, width=32)
    caixa_cliente.grid(row=2, column=1, pady=5)

    # ---- Campos de data e horario ----
    tk.Label(quadro, text="Data (AAAA-MM-DD):").grid(row=3, column=0, sticky="w", pady=5)
    entrada_data = tk.Entry(quadro, width=35)
    entrada_data.grid(row=3, column=1, pady=5)

    tk.Label(quadro, text="Hora inicio (HH:MM):").grid(row=4, column=0, sticky="w", pady=5)
    entrada_inicio = tk.Entry(quadro, width=35)
    entrada_inicio.grid(row=4, column=1, pady=5)

    tk.Label(quadro, text="Hora fim (HH:MM):").grid(row=5, column=0, sticky="w", pady=5)
    entrada_fim = tk.Entry(quadro, width=35)
    entrada_fim.grid(row=5, column=1, pady=5)

    tk.Label(quadro, text="(minimo 30min, maximo 4h, seg a sex das 08h as 18h)",
             font=("Arial", 9), fg="gray").grid(row=6, column=0, columnspan=2, pady=5)

    def confirmar():
        # MAIS PARA FRENTE, aqui vamos:
        #   1) descobrir o id da sala e do cliente que foram escolhidos,
        #   2) checar as regras (horario livre, duracao, dias e horas permitidos),
        #   3) e so entao chamar bd.cadastrar_reserva(...).
        messagebox.showinfo("A fazer", "A logica de salvar a reserva sera feita na proxima etapa.")

    tk.Button(quadro, text="Confirmar", width=20, bg="#1f4fc4", fg="white",
              command=confirmar).grid(row=7, column=0, columnspan=2, pady=20)
