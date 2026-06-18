# ============================================================
# TELA DASHBOARD (tela inicial, depois do login)
# Tela criada por Dener em 17/06/2026
# ------------------------------------------------------------
# E o "menu principal" do sistema. Mostra um resumo da ocupacao
# das salas e tem botoes para abrir as outras telas.
# ============================================================

import tkinter as tk


def montar_dashboard(container, navegar):
    # limpa a tela anterior
    for widget in container.winfo_children():
        widget.destroy()

    # ---- Cabecalho ----
    tk.Label(container, text="ShareSpace - Painel", font=("Arial", 22, "bold")).pack(pady=15)

    # ---- Area dos indicadores (numeros de resumo) ----
    # POR ENQUANTO os numeros sao de exemplo. MAIS PARA FRENTE eles virao
    # de contas feitas em cima da tabela "reserva" do banco de dados.
    quadro_info = tk.Frame(container)
    quadro_info.pack(pady=10)

    tk.Label(quadro_info, text="Ocupacao geral: 62%", font=("Arial", 14)).grid(row=0, column=0, padx=20)
    tk.Label(quadro_info, text="Salas disponiveis: 38%", font=("Arial", 14)).grid(row=0, column=1, padx=20)
    tk.Label(quadro_info, text="Salas em manutencao: 1", font=("Arial", 14)).grid(row=0, column=2, padx=20)

    # ---- Botoes do menu (abrem as outras telas) ----
    quadro_menu = tk.Frame(container)
    quadro_menu.pack(pady=30)

    # Esta lista guarda: (texto que aparece no botao, nome da tela que ele abre).
    botoes = [
        ("Buscar Salas",            "busca"),
        ("Cadastrar Sala",          "cadastro_sala"),
        ("Cadastrar Cliente",       "cadastro_cliente"),
        ("Historico de Reservas",   "historico"),
        ("Backup / Configuracoes",  "backup"),
    ]

    # Aqui montamos os botoes em um laco (for) para nao repetir codigo.
    linha = 0
    for texto, nome_tela in botoes:
        # ATENCAO ao "t=nome_tela": isso faz cada botao guardar o SEU proprio nome
        # de tela. Sem isso, todos os botoes acabariam abrindo a mesma tela (a ultima).
        tk.Button(quadro_menu, text=texto, width=25, height=2, bg="#1f4fc4", fg="white",
                  command=lambda t=nome_tela: navegar(t)).grid(row=linha, column=0, pady=5)
        linha = linha + 1

    # Botao de sair (volta para o login)
    tk.Button(container, text="Sair", command=lambda: navegar("login")).pack(pady=10)
