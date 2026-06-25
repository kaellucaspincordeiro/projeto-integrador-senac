# ============================================================
# TELA DE HISTORICO DE RESERVAS  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Tabela estilizada (cabecalho azul + linhas zebra) que cresce
# junto com a janela.
# Modificado por Fernando (23/06/2026) - Ajustes de ortografia e layout.
# Modificações feitas por Dener (25/06/2026)
#   - FILTROS por Sala, Cliente, Status e Data (listas montadas a partir das
#     proprias reservas existentes).
#   - Botao "Cancelar reserva": marca a reserva selecionada como 'cancelada'
#     (ela some das salas ocupadas, mas continua no historico).
#   - Mostra a contagem de reservas encontradas.
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import banco_dados as bd
import ui


def montar_historico(container, navegar):
    ui.limpar(container)
    corpo = ui.barra_topo(container, "Histórico de Reservas",
                          lambda: navegar("dashboard"))

    # Reservas: (id, sala, cliente, data, inicio, fim, status, criado_em)
    todas = bd.db_listar_reservas()

    # ---- Card de filtros ----
    filtros = ui.card(corpo)
    filtros.pack(fill="x", pady=(0, 10))
    fi = tk.Frame(filtros, bg=ui.COR_CARD)
    fi.pack(fill="x", padx=18, pady=14)

    def lista_combo(parent, rotulo, valores, largura):
        quadro = tk.Frame(parent, bg=ui.COR_CARD)
        quadro.pack(side="left", padx=(0, 16))
        combo = ui.campo(quadro, rotulo, valores=valores, largura=largura)
        combo.set(valores[0])
        combo.config(state="readonly")   # so deixa escolher da lista
        return combo

    salas = sorted({r[1] for r in todas})
    clientes = sorted({r[2] for r in todas})
    datas = sorted({r[3] for r in todas})

    combo_sala = lista_combo(fi, "SALA", ["Todas"] + salas, 16)
    combo_cliente = lista_combo(fi, "CLIENTE", ["Todos"] + clientes, 16)
    combo_status = lista_combo(fi, "STATUS", ["Todos", "Ativa", "Cancelada"], 12)
    combo_data = lista_combo(fi, "DATA", ["Todas"] + datas, 14)

    f_btn = tk.Frame(fi, bg=ui.COR_CARD)
    f_btn.pack(side="left", anchor="s")
    ui.botao(f_btn, "Filtrar", lambda: aplicar(), icone_nome="busca").pack(side="left")
    ui.botao(f_btn, "Limpar", lambda: limpar(), variante="neutro").pack(side="left", padx=(8, 0))

    # ---- Tabela ----
    cartao = ui.card(corpo)
    cartao.pack(fill="both", expand=True)
    cartao.rowconfigure(0, weight=1)
    cartao.columnconfigure(0, weight=1)

    colunas = ("id", "sala", "cliente", "data", "início", "fim", "status", "criado_em")
    tabela = ttk.Treeview(cartao, columns=colunas, show="headings")
    larguras = {"id": 50, "sala": 150, "cliente": 160, "data": 100,
                "início": 80, "fim": 80, "status": 110, "criado_em": 150}
    for c in colunas:
        tabela.heading(c, text=c.replace("_", " ").capitalize())
        tabela.column(c, width=larguras.get(c, 100), anchor="center")

    scroll = ttk.Scrollbar(cartao, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)
    tabela.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
    scroll.grid(row=0, column=1, sticky="ns", pady=10, padx=(0, 10))

    # ---- Rodape: contagem + cancelar ----
    rodape = tk.Frame(corpo, bg=ui.COR_FUNDO)
    rodape.pack(fill="x", pady=(8, 0))
    lbl_total = ui.lbl(rodape, "", fonte=ui.F_PEQ, fg=ui.COR_TEXTO_FRACO, bg=ui.COR_FUNDO)
    lbl_total.pack(side="left")
    ui.botao(rodape, "Cancelar reserva", lambda: cancelar(),
             variante="perigo").pack(side="right")

    # ------------------------------------------------------------
    # Logica
    # ------------------------------------------------------------
    def mostrar(linhas):
        tabela.delete(*tabela.get_children())
        ui.zebrar(tabela, linhas)
        lbl_total.config(text=f"{len(linhas)} reserva(s) encontrada(s)")

    def aplicar():
        sala = combo_sala.get()
        cliente = combo_cliente.get()
        status = combo_status.get().lower()
        data = combo_data.get()

        filtradas = []
        for r in todas:
            if sala != "Todas" and r[1] != sala:
                continue
            if cliente != "Todos" and r[2] != cliente:
                continue
            if status != "todos" and r[6] != status:
                continue
            if data != "Todas" and r[3] != data:
                continue
            filtradas.append(r)
        mostrar(filtradas)

    def limpar():
        combo_sala.set("Todas")
        combo_cliente.set("Todos")
        combo_status.set("Todos")
        combo_data.set("Todas")
        aplicar()

    def cancelar():
        nonlocal todas
        selecao = tabela.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecione uma reserva na tabela.")
            return
        valores = tabela.item(selecao[0], "values")
        id_reserva, status_atual = valores[0], valores[6]
        if status_atual == "cancelada":
            messagebox.showinfo("Aviso", "Esta reserva já está cancelada.")
            return
        if messagebox.askyesno("Confirmar", "Deseja cancelar esta reserva?"):
            bd.cancelar_reserva(id_reserva)
            todas = bd.db_listar_reservas()   # recarrega com o status novo
            aplicar()

    # Primeira carga: mostra tudo.
    aplicar()
