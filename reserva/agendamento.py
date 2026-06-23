# ============================================================
# TELA DE AGENDAMENTO (criar uma reserva)
# Tela criada por Dener em 17/06/2026
# ------------------------------------------------------------
# Aqui escolhemos a sala, o cliente, a data e o horario da reserva.
#
# As REGRAS (nao deixar horario repetido, reserva de 30min a 4h,
# so de segunda a sexta das 08h as 18h, sem data no passado)
# vamos programar na proxima etapa.
# Kael: Adicionando as funções para atender o def confirmar() e uma tabela das reservas
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
        sala = caixa_sala.get()
        cliente = caixa_cliente.get()
        data = entrada_data.get()
        hora_inicio = entrada_inicio.get()
        hora_fim = entrada_fim.get()

        duracao = hora_fim - hora_inicio

        def horas_permitidos(hora_inicio, hora_fim):
            if hora_inicio < "08:00" or hora_fim > "18:00":
                return False
            return True

        if sala == "" or cliente == "" or data == "" or hora_inicio == "" or hora_fim == "":
            messagebox.showwarning("Atencao", "Preencha todos os campos para o agendamento.")
            return

        agendamento = bd.cadastrar_reserva(
            sala, cliente, data, hora_inicio, hora_fim)

        if agendamento and duracao and horas_permitidos(hora_inicio, hora_fim):
            messagebox.showinfo("Sucesso", "Reserva cadastrada!")
        else:
            messagebox.showinfo("Erro", "Problema ao cadastrar a reserva.")

    tk.Button(quadro, text="Confirmar", width=20, bg="#1f4fc4", fg="white",
              command=confirmar).grid(row=7, column=0, columnspan=2, pady=20)
    
    frame_tabela_reserva = tk.Frame(container)
    frame_tabela_reserva.grid(row=9, column=0, pady=15, padx=20, sticky="nsew")

    colunas = ("id", "sala", "cliente", "data", "inicio", "fim")

    tabela = ttk.Treeview(
        frame_tabela_reserva,
        columns=colunas,
        show="headings",
        height=7
    )

    # Cabeçalhos
    tabela.heading("id", text="Id")
    tabela.heading("sala", text="Sala")
    tabela.heading("cliente", text="Cliente")
    tabela.heading("data", text="Data")
    tabela.heading("inicio", text="Início")
    tabela.heading("fim", text="Fim")

    # Tamanho das colunas
    tabela.column("id", width=50, anchor="center")
    tabela.column("sala", width=100, anchor="center")
    tabela.column("cliente", width=100, anchor="center")
    tabela.column("data", width=100, anchor="center")
    tabela.column("inicio", width=100, anchor="center")
    tabela.column("fim", width=100, anchor="center")

    # Scrollbar vertical
    scroll_y = ttk.Scrollbar(
        frame_tabela_reserva,
        orient="vertical",
        command=tabela.yview
    )

    tabela.configure(yscrollcommand=scroll_y.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")

    # Permite a tabela expandir dentro do frame
    frame_tabela_reserva.grid_rowconfigure(0, weight=1)
    frame_tabela_reserva.grid_columnconfigure(0, weight=1)

    # --- CARREGAR DADOS NA TABELA ---
    reservas = bd.db_listar_reservas()

    for linha in reservas:
        tabela.insert("", "end", values=linha)
