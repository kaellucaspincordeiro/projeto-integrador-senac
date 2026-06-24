# ============================================================
# TELA DE CADASTRO DE EQUIPAMENTO  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Mesmo layout de duas areas: formulario a esquerda, tabela a
# direita (cresce com a janela).
# Modificado por Fernando (23/06/2026) - Ajustes de ortografia e layout.
# ============================================================

import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd
import ui


def montar_cadastro_equipamento(container, navegar):
    ui.limpar(container)
    corpo = ui.barra_topo(container, "Cadastro de Equipamento",
                          lambda: navegar("dashboard"))
    corpo.columnconfigure(1, weight=1)
    corpo.rowconfigure(0, weight=1)

    # ---- Formulario (esquerda) ----
    form = ui.card(corpo)
    form.grid(row=0, column=0, sticky="n", padx=(0, 18))
    interno = tk.Frame(form, bg=ui.COR_CARD)
    interno.pack(padx=28, pady=24)
    ui.lbl(interno, "Novo equipamento", fonte=ui.F_H2).pack(anchor="w", pady=(0, 4))

    ent_nome = ui.campo(interno, "NOME DO EQUIPAMENTO", largura=28)
    ent_quantidade = ui.campo(interno, "QUANTIDADE DISPONÍVEL", largura=28)

    def salvar_equipamento():
        nome = ent_nome.get()
        quantidade = ent_quantidade.get()
        if nome.isalpha() == "" or quantidade.isalpha() == "":
            messagebox.showwarning("Atenção",
                                   "Preencha pelo menos o Nome e a Quantidade do Equipamento.")
            return
        if bd.cadastrar_equipamento(nome, quantidade):
            messagebox.showinfo("Sucesso", "Equipamento cadastrado!")
        else:
            messagebox.showerror("Erro", "Já existe um equipamento cadastrado.")

    def deletar_equipamento():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um equipamento na tabela.")
            return
        id_equip = tabela.item(item, "values")[0]
        if messagebox.askyesno("Confirmar", "Deseja excluir este equipamento?"):
            bd.deletar_equipamento(id_equip)
            tabela.delete(item)

    acoes = tk.Frame(interno, bg=ui.COR_CARD)
    acoes.pack(fill="x", pady=(20, 0))
    ui.botao(acoes, "Salvar", salvar_equipamento, variante="sucesso",
             icone_nome="disponivel").pack(side="left")
    ui.botao(acoes, "Editar", lambda: None, variante="neutro").pack(side="left", padx=8)
    ui.botao(acoes, "Excluir", deletar_equipamento, variante="perigo").pack(side="left")

    # ---- Tabela (direita) ----
    bloco = ui.card(corpo)
    bloco.grid(row=0, column=1, sticky="nsew")
    bloco.rowconfigure(0, weight=1)
    bloco.columnconfigure(0, weight=1)

    colunas = ("id", "equipamento", "quantidade")
    titulos = ("Id", "Nome do Equipamento", "Quantidade Disponível")
    larguras = (50, 220, 160)
    tabela = ttk.Treeview(bloco, columns=colunas, show="headings")
    for c, t, w in zip(colunas, titulos, larguras):
        tabela.heading(c, text=t)
        tabela.column(c, width=w, anchor="center")

    scroll = ttk.Scrollbar(bloco, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)
    tabela.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
    scroll.grid(row=0, column=1, sticky="ns", pady=10, padx=(0, 10))

    ui.zebrar(tabela, bd.listar_equipamentos())
