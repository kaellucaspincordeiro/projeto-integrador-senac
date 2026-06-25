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
# Modificações feitas por Dener (25/06/2026)
#   - Correção do status invalido ("ativa" -> "disponivel") que impedia salvar.
#   - Agora a sala pode ser cadastrada JA com varios equipamentos disponiveis:
#     lista com selecao (checkbox) + quantidade de cada um, gravados na mesma
#     transacao (tabela sala_equipamento).
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
    # O formulario fica numa AREA ROLAVEL e os botoes (Salvar/Editar/Excluir)
    # numa BARRA FIXA embaixo do card. Assim, por mais campos/equipamentos que
    # existam, o botao Salvar aparece SEMPRE (antes ele sumia quando a lista de
    # equipamentos deixava o formulario mais alto que a tela).
    form = ui.card(corpo)
    form.grid(row=0, column=0, sticky="ns", padx=(0, 18))
    form.rowconfigure(0, weight=1)      # a area rolavel estica
    form.columnconfigure(0, weight=1)

    canvas_form = tk.Canvas(form, bg=ui.COR_CARD, highlightthickness=0, width=360)
    rolagem = ttk.Scrollbar(form, orient="vertical", command=canvas_form.yview)
    canvas_form.configure(yscrollcommand=rolagem.set)
    canvas_form.grid(row=0, column=0, sticky="nsew")
    rolagem.grid(row=0, column=1, sticky="ns")

    area = tk.Frame(canvas_form, bg=ui.COR_CARD)   # frame que rola dentro do canvas
    janela_area = canvas_form.create_window((0, 0), window=area, anchor="nw")
    area.bind("<Configure>",
              lambda e: canvas_form.configure(scrollregion=canvas_form.bbox("all")))
    canvas_form.bind("<Configure>",
                     lambda e: canvas_form.itemconfig(janela_area, width=e.width))

    # Rolagem com a roda do mouse (com guarda p/ nao quebrar ao trocar de tela).
    def _roda(e):
        if canvas_form.winfo_exists():
            canvas_form.yview_scroll(int(-e.delta / 120), "units")
    canvas_form.bind("<Enter>", lambda e: canvas_form.bind_all("<MouseWheel>", _roda))
    canvas_form.bind("<Leave>", lambda e: canvas_form.unbind_all("<MouseWheel>"))

    interno = tk.Frame(area, bg=ui.COR_CARD)
    interno.pack(fill="both", expand=True, padx=28, pady=24)
    ui.lbl(interno, "Nova sala", fonte=ui.F_H2).pack(anchor="w", pady=(0, 4))

    ent_nome = ui.campo(interno, "NOME DA SALA", largura=28)
    ent_numero = ui.campo(interno, "NÚMERO DA SALA", largura=28)
    ent_andar = ui.campo(interno, "ANDAR DA SALA", largura=28)
    ent_capacidade = ui.campo(interno, "CAPACIDADE", largura=28)
    ent_observacao = ui.campo(interno, "OBSERVAÇÕES", largura=28)

    # ---- Equipamentos disponiveis para associar a sala ----
    # Mostra os equipamentos do banco. O usuario marca os que a sala tem e
    # informa a quantidade de cada um. Pode marcar VARIOS de uma vez.
    ui.lbl(interno, "EQUIPAMENTOS DA SALA", fonte=ui.F_LABEL,
           fg=ui.COR_TEXTO_FRACO).pack(anchor="w", pady=(12, 2))

    equipamentos = bd.listar_equipamentos()   # (id, nome, quantidade_disponivel)
    linhas_equip = []   # cada item: (id_equip, nome, var_marcado, entry_qtd, disponivel)

    if not equipamentos:
        ui.lbl(interno, "Nenhum equipamento cadastrado ainda.\nCadastre equipamentos primeiro.",
               fonte=ui.F_PEQ, fg=ui.COR_TEXTO_FRACO, justify="left").pack(anchor="w")
    else:
        # Quadro com a lista de equipamentos (a rolagem fica por conta do
        # formulario inteiro, entao aqui basta empilhar as linhas).
        caixa = tk.Frame(interno, bg=ui.COR_CARD, highlightbackground=ui.COR_BORDA,
                         highlightthickness=1)
        caixa.pack(fill="x", pady=(2, 0))

        for id_equip, nome_equip, disponivel in equipamentos:
            linha = tk.Frame(caixa, bg=ui.COR_CARD)
            linha.pack(fill="x", padx=8, pady=3)
            marcado = tk.BooleanVar(value=False)
            tk.Checkbutton(linha, text=f"{nome_equip}  (disp.: {disponivel})",
                           variable=marcado, bg=ui.COR_CARD, fg=ui.COR_TEXTO,
                           activebackground=ui.COR_CARD, selectcolor=ui.COR_PRIM_CLARA,
                           anchor="w").pack(side="left")
            ent_qtd = ttk.Entry(linha, width=5, justify="center")
            ent_qtd.insert(0, "1")
            ent_qtd.pack(side="right")
            ui.lbl(linha, "Qtd", fonte=ui.F_PEQ, fg=ui.COR_TEXTO_FRACO).pack(side="right", padx=(0, 4))
            linhas_equip.append((id_equip, nome_equip, marcado, ent_qtd, disponivel))

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

        # 3. Coleta os equipamentos MARCADOS, com a quantidade de cada um.
        equipamentos_escolhidos = []
        for id_equip, nome_equip, marcado, ent_qtd, disponivel in linhas_equip:
            if not marcado.get():
                continue
            qtd_texto = ent_qtd.get().strip()
            if not qtd_texto.isdigit() or int(qtd_texto) <= 0:
                messagebox.showwarning("Atenção",
                    f"Quantidade inválida para o equipamento '{nome_equip}'.\n"
                    "Use um número inteiro maior que 0.")
                return
            qtd = int(qtd_texto)
            if qtd > disponivel:
                messagebox.showwarning("Atenção",
                    f"O equipamento '{nome_equip}' tem apenas {disponivel} disponível(is).")
                return
            equipamentos_escolhidos.append((id_equip, qtd))

        # 4. Salva a sala E as associacoes numa unica transacao (tudo ou nada).
        try:
            bd.cadastrar_sala_com_equipamentos(
                nome, numero, andar, capacidade, observacao, "disponivel",
                equipamentos_escolhidos)

            if equipamentos_escolhidos:
                messagebox.showinfo("Sucesso",
                    f"Sala cadastrada com {len(equipamentos_escolhidos)} equipamento(s) associado(s)!")
            else:
                messagebox.showinfo("Sucesso", "Sala cadastrada com sucesso!")

            # Limpa os campos do formulário para o próximo cadastro
            ent_nome.delete(0, tk.END)
            ent_numero.delete(0, tk.END)
            ent_andar.delete(0, tk.END)
            ent_capacidade.delete(0, tk.END)
            ent_observacao.delete(0, tk.END)

            # Desmarca os equipamentos e volta a quantidade para 1
            for _id, _nome, marcado, ent_qtd, _disp in linhas_equip:
                marcado.set(False)
                ent_qtd.delete(0, tk.END)
                ent_qtd.insert(0, "1")

            # Atualiza a tabela na tela imediatamente com os dados novos
            ui.zebrar(tabela, bd.listar_salas())

        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível registrar a sala:\n{erro}")

    def excluir_sala():
        selecao = tabela.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecione uma sala na tabela.")
            return
        item = selecao[0]
        id_sala = tabela.item(item, "values")[0]
        if messagebox.askyesno("Confirmar", "Deseja excluir esta sala?"):
            bd.deletar_sala(id_sala)
            tabela.delete(item)

    # Barra de acoes FIXA no rodape do card (fora da area rolavel), para o
    # botao Salvar estar sempre visivel.
    acoes = tk.Frame(form, bg=ui.COR_CARD)
    acoes.grid(row=1, column=0, columnspan=2, sticky="ew", padx=28, pady=(8, 18))
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
