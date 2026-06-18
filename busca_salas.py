# ============================================================
# TELA DE BUSCA DE SALAS
# Tela criada por Dener em 17/06/2026
# ------------------------------------------------------------
# Aqui o administrador escolhe a data e o horario e o sistema
# mostra quais salas estao livres. Tambem da para filtrar por
# capacidade e por equipamento.
#
# A ordem que os requisitos pedem e:
#   1) disponiveis primeiro
#   2) depois as indisponiveis
#   3) por ultimo as que estao em manutencao
#
# POR ENQUANTO os resultados sao de exemplo (escritos na mao).
# MAIS PARA FRENTE eles virao do banco de dados.
# ============================================================

import tkinter as tk


def montar_busca_salas(container, navegar):
    # limpa a tela anterior
    for widget in container.winfo_children():
        widget.destroy()

    tk.Button(container, text="< Voltar", bg="#1f4fc4", fg="white",
              command=lambda: navegar("dashboard")).pack(anchor="w", padx=10, pady=10)

    tk.Label(container, text="Busca de Salas", font=("Arial", 18, "bold")).pack(pady=(0, 10))

    # ---- Filtros (data, horario) ----
    filtros = tk.Frame(container)
    filtros.pack(pady=10)

    tk.Label(filtros, text="Data:").grid(row=0, column=0, padx=5)
    tk.Entry(filtros, width=12).grid(row=0, column=1, padx=5)   # exemplo: 2026-06-20

    tk.Label(filtros, text="Inicio:").grid(row=0, column=2, padx=5)
    tk.Entry(filtros, width=8).grid(row=0, column=3, padx=5)    # exemplo: 09:00

    tk.Label(filtros, text="Fim:").grid(row=0, column=4, padx=5)
    tk.Entry(filtros, width=8).grid(row=0, column=5, padx=5)    # exemplo: 10:30

    # MAIS PARA FRENTE: o botao BUSCAR vai procurar no banco as salas livres.
    tk.Button(filtros, text="BUSCAR", bg="#1f4fc4", fg="white").grid(row=0, column=6, padx=10)

    # ---- Resultados (exemplo) ----
    resultados = tk.Frame(container)
    resultados.pack(pady=10, fill="x", padx=20)

    # Grupo: DISPONIVEIS (verde)
    tk.Label(resultados, text="DISPONIVEIS", font=("Arial", 12, "bold"), fg="green").pack(anchor="w")
    linha = tk.Frame(resultados)
    linha.pack(fill="x", pady=2)
    tk.Label(linha, text="Sala Alfa (101, 1o andar, 8 lugares)").pack(side="left")
    # O botao Reservar leva para a tela de agendamento.
    tk.Button(linha, text="Reservar", command=lambda: navegar("agendamento")).pack(side="right")

    # Grupo: INDISPONIVEIS (laranja)
    tk.Label(resultados, text="INDISPONIVEIS", font=("Arial", 12, "bold"),
             fg="orange").pack(anchor="w", pady=(10, 0))
    tk.Label(resultados, text="Sala Beta (502) - ocupada das 14h as 17h").pack(anchor="w")

    # Grupo: EM MANUTENCAO (vermelho)
    tk.Label(resultados, text="EM MANUTENCAO", font=("Arial", 12, "bold"),
             fg="red").pack(anchor="w", pady=(10, 0))
    tk.Label(resultados, text="Sala Gama (1503)").pack(anchor="w")
