# ============================================================
# TELA DE CADASTRO DE SALA  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Layout de duas areas: formulario a esquerda e a tabela de salas
# a direita (a tabela cresce junto com a janela).
# Modificado por Fernando (23/06/2026) - Ajustes de ortografia e layout.
# Modificações feitas por Fernando (25/06/2026)
#   - Implementada a logica de salvar e excluir salas.
#   - Garante que o ANDAR e a CAPACIDADE sejam números inteiros.
#   - Realiza a INSERÇÃO no banco de dados e ATUALIZA a tabela na tela.
#   - Limpa automaticamente os campos do formulario apos salvar.
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
        nome = ent_nome.get().strip()
        numero = ent_numero.get().strip()
        andar_texto = ent_andar.get().strip()
        capacidade_texto = ent_capacidade.get().strip()
        observacao = ent_observacao.get().strip()
        
        # 1. Validação de campos vazios
        if nome == "" or numero == "" or andar_texto == "" or capacidade_texto == "":
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios da sala.")
            return
        
        # 2. Regra: Andar e Capacidade devem ser inteiros
        if not andar_texto.isdigit() or not capacidade_texto.isdigit():
            messagebox.showwarning("Atenção", "Os campos 'ANDAR' e 'CAPACIDADE' devem ser números inteiros!")
            return
        
        andar = int(andar_texto)
        capacidade = int(capacidade_texto)

        # POP-UPS de aviso para limites de andar e capacidade
        if not (1 <= andar <= 15):
            messagebox.showwarning("Aviso de Limite", "O prédio possui apenas 15 andares.\nPor favor, digite um andar entre 1 e 15.")
            return

        if capacidade <= 0:
            messagebox.showwarning("Atenção", "A capacidade da sala deve ser maior que 0.")
            return

        # 3. Salva no Banco de Dados
        try:
            bd.cadastrar_sala(nome, numero, andar, capacidade, observacao, "ativa")
            
            messagebox.showinfo("Sucesso", "Sala cadastrada com sucesso!")
            
            # Limpa os campos do formulário para o próximo cadastro
            ent_nome.delete(0, tk.END)
            ent_numero.delete(0, tk.END)
            ent_andar.delete(0, tk.END)
            ent_capacidade.delete(0, tk.END)
            ent_observacao.delete(0, tk.END)
            
            # Atualiza a tabela na tela imediatamente com os dados novos
            ui.zebrar(tabela, bd.listar_salas())
            
        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível registrar a sala:\n{erro}")

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
