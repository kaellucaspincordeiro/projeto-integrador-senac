import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd

# Melhoria feita por Dener em 17/06/2026
# Corrigi dois problemas nesta tela:
# 1) Tirei o "container.geometry(...)". O geometry() so existe na JANELA (Tk/Toplevel), nao em um Frame.
#    Quem deve definir o tamanho e a janela principal (no main.py), nao esta tela.
# 2) Os campos "Nome da Sala" e "Capacidade" estavam na MESMA linha do grid (os dois em row=2 e row=3),
#    entao ficavam um em cima do outro. Coloquei a Capacidade nas linhas de baixo (row 4 e 5) e o
#    botao Salvar na linha 6, assim cada campo fica um embaixo do outro.
# Kael: Correção e adição dos campos contidos da tabela sala
def montar_cadastrar_sala(container, funcao_voltar):
    for widget in container.winfo_children():
        widget.destroy()

    container.grid_columnconfigure(0, weight=1)

# --- BOTÃO VOLTAR ---
    # Ele fica no topo para fácil acesso
    tk.Button(container, text="← Voltar", command=funcao_voltar, bg="#1f4fc4", fg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    
    frame_cadastra_sala = tk.Frame(container)
    frame_cadastra_sala.grid(row=1, column=0, pady=10)

    tk.Label(frame_cadastra_sala, text="ShareSpace", font=("Arial", 24, "bold")).grid(row=0, column=0, pady=(0, 15))
    tk.Label(frame_cadastra_sala, text="Cadastro de Sala", font=("Arial", 16, "bold")).grid(row=1, column=0, pady=(0, 15))
    
    tk.Label(frame_cadastra_sala, text="Nome da Sala:", font=("Arial", 15, "bold")).grid(row=2, column=0, pady=(0, 5))
    ent_nome_sala = tk.Entry(frame_cadastra_sala, width=40)
    ent_nome_sala.grid(row=3, column=0, pady=(0, 10))

    tk.Label(frame_cadastra_sala, text="Número da Sala:", font=("Arial", 15, "bold")).grid(row=4, column=0, pady=(0, 5))
    ent_numero = tk.Entry(frame_cadastra_sala, width=40)
    ent_numero.grid(row=5, column=0, pady=(0, 10))

    tk.Label(frame_cadastra_sala, text="Andar da Sala:", font=("Arial", 15, "bold")).grid(row=6, column=0, pady=(0, 5))
    ent_andar = tk.Entry(frame_cadastra_sala, width=40)
    ent_andar.grid(row=7, column=0, pady=(0, 10))

    tk.Label(frame_cadastra_sala, text="Capacidade:", font=("Arial", 15, "bold")).grid(row=8, column=0, pady=(0, 5))
    ent_capacidade = tk.Entry(frame_cadastra_sala, width=40)
    ent_capacidade.grid(row=9, column=0, pady=(0, 10))

    tk.Label(frame_cadastra_sala, text="Observações:", font=("Arial", 15, "bold")).grid(row=10, column=0, pady=(0, 5))
    ent_observacao = tk.Entry(frame_cadastra_sala, width=40)
    ent_observacao.grid(row=11, column=0, pady=(0, 10))

    def salvar_sala():
        nome = ent_nome_sala.get()
        numero = ent_numero.get()
        andar = ent_andar.get()
        capacidade = ent_capacidade.get()
        observacao = ent_observacao.get()

        if nome == "" or numero == "" or andar == "" or capacidade == "" or observacao == "":
            messagebox.showwarning("Atencao", "Preencha os campos da sala.")
            return

        cadastrar_sala = bd.cadastrar_sala(
            nome, numero, andar, capacidade, observacao)

        if cadastrar_sala:
            messagebox.showinfo("Sucesso", "Sala cadastrada!")
        else:
            messagebox.showerror("Erro", "Ja existe uma sala registrada.")


    tk.Button(frame_cadastra_sala, text="Salvar", command=salvar_sala, bg="#1f4fc4", fg="white").grid(row=12, column=0, pady=(0, 15))
    tk.Button(frame_cadastra_sala, text="Editar", bg="#1f4fc4", fg="white").grid(row=13, column=0, pady=(0, 15))
    tk.Button(frame_cadastra_sala, text="Excluir", bg="#d32d2d", fg="black").grid(row=14, column=0, pady=(0, 15))

    frame_tabela_sala = tk.Frame(container)
    frame_tabela_sala.grid(row=16, column=0, pady=15, padx=20, sticky="nsew")

    colunas = ("id", "nome", "numero", "andar", "capacidade", "observacao", "status")

    tabela = ttk.Treeview(
        frame_tabela_sala,
        columns=colunas,
        show="headings",
        height=8
    )

    # Cabeçalhos
    tabela.heading("id", text="Id")
    tabela.heading("nome", text="Nome da Sala")
    tabela.heading("numero", text="Número da Sala")
    tabela.heading("andar", text="Andar da Sala")
    tabela.heading("capacidade", text="Capacidde")
    tabela.heading("observacao", text="Observações")
    tabela.heading("status", text="Status")

    # Tamanho das colunas
    tabela.column("id", width=50, anchor="center")
    tabela.column("nome", width=50, anchor="center")
    tabela.column("numero", width=20, anchor="center")
    tabela.column("andar", width=20, anchor="center")
    tabela.column("capacidade", width=20, anchor="center")
    tabela.column("observacao", width=100, anchor="center")
    tabela.column("status", width=30, anchor="center")

    # Scrollbar vertical
    scroll_y = ttk.Scrollbar(
        frame_tabela_sala,
        orient="vertical",
        command=tabela.yview
    )

    tabela.configure(yscrollcommand=scroll_y.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")

    # Permite a tabela expandir dentro do frame
    frame_tabela_sala.grid_rowconfigure(0, weight=1)
    frame_tabela_sala.grid_columnconfigure(0, weight=1)

    # --- CARREGAR DADOS NA TABELA ---
    salas = bd.listar_salas()

    for linha in salas:
        tabela.insert("", "end", values=linha)




