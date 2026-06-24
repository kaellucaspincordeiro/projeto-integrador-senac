# ============================================================
# TELA DE CADASTRO DE SALA  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Layout de duas areas: formulario a esquerda e a tabela de salas
# a direita (a tabela cresce junto com a janela).
# Modificado por Fernando (23/06/2026) - Ajustes de ortografia e layout.
# ============================================================

import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd
import ui


def montar_cadastrar_sala(container, funcao_voltar):
    ui.limpar(container)
    corpo = ui.barra_topo(container, "Cadastro de Sala", funcao_voltar)
    corpo.columnconfigure(1, weight=1)   # a coluna da tabela estica
    corpo.rowconfigure(0, weight=1)

    # ---- Formulario (esquerda) ----
    form = ui.card(corpo)
    form.grid(row=0, column=0, sticky="n", padx=(0, 18))
    interno = tk.Frame(form, bg=ui.COR_CARD)
    interno.pack(padx=28, pady=24)
    ui.lbl(interno, "Nova sala", fonte=ui.F_H2).pack(anchor="w", pady=(0, 4))

    ent_nome = ui.campo(interno, "NOME DA SALA", largura=28)
    ent_numero = ui.campo(interno, "NÚMERO DA SALA", largura=28)
    ent_andar = ui.campo(interno, "ANDAR DA SALA", largura=28)
    ent_capacidade = ui.campo(interno, "CAPACIDADE", largura=28)
    ent_observacao = ui.campo(interno, "OBSERVAÇÕES", largura=28)

    def salvar_sala():
        nome = ent_nome.get()
        numero = ent_numero.get()
        andar = ent_andar.get()
        capacidade = ent_capacidade.get()
        observacao = ent_observacao.get()
        if nome.isalpha() == "" or numero.isnumeric() == "" or andar.isalpha() == "" or int(capacidade) == "" or observacao.isalpha() == "":
            messagebox.showwarning("Atenção", "Preencha os campos da sala.")
            return
        if bd.cadastrar_sala(nome, numero, andar, capacidade, observacao):
            messagebox.showinfo("Sucesso", "Sala cadastrada!")
        else:
            messagebox.showerror("Erro", "Já existe uma sala registrada.")

    def excluir_sala():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma sala na tabela.")
            return
        id_sala = tabela.item(item, "values")[0]
        if messagebox.askyesno("Confirmar", "Deseja excluir esta sala?"):
            bd.deletar_sala(id_sala)
            tabela.delete(item)

    acoes = tk.Frame(interno, bg=ui.COR_CARD)
    acoes.pack(fill="x", pady=(20, 0))
    ui.botao(acoes, "Salvar", salvar_sala, variante="sucesso",
             icone_nome="disponivel").pack(side="left")
    ui.botao(acoes, "Editar", lambda: None, variante="neutro").pack(side="left", padx=8)
    ui.botao(acoes, "Excluir", excluir_sala, variante="perigo").pack(side="left")

    # ---- Tabela (direita) ----
    bloco = ui.card(corpo)
    bloco.grid(row=0, column=1, sticky="nsew")
    bloco.rowconfigure(0, weight=1)
    bloco.columnconfigure(0, weight=1)

    colunas = ("id", "nome", "numero", "andar", "capacidade", "observacao", "status")
    titulos = ("Id", "Nome", "Número", "Andar", "Capac.", "Observações", "Status")
    larguras = (50, 130, 80, 70, 70, 160, 90)
    tabela = ttk.Treeview(bloco, columns=colunas, show="headings")
    for c, t, w in zip(colunas, titulos, larguras):
        tabela.heading(c, text=t)
        tabela.column(c, width=w, anchor="center")

    scroll = ttk.Scrollbar(bloco, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)
    tabela.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
    scroll.grid(row=0, column=1, sticky="ns", pady=10, padx=(0, 10))

    ui.zebrar(tabela, bd.listar_salas())
