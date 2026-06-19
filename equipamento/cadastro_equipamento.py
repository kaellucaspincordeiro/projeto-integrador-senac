import tkinter as tk
from tkinter import messagebox, ttk
import banco_dados as bd

# Feito por Kael na tela do cadastro de equipamento
def montar_cadastro_equipamento(container, navegar):
    for widget in container.winfo_children():
        widget.destroy()

    container.grid_columnconfigure(0, weight=1)

# --- BOTÃO VOLTAR ---
    # Ele fica no topo para fácil acesso
    tk.Button(container, text="← Voltar", command=lambda: navegar("dashboard"), bg="#1f4fc4", fg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    
    frame_cadastro_equipamento = tk.Frame(container)
    frame_cadastro_equipamento.grid(row=1, column=0, pady=10)

    tk.Label(frame_cadastro_equipamento, text="ShareSpace", font=("Arial", 24, "bold")).grid(row=0, column=0, pady=(0, 15))
    tk.Label(frame_cadastro_equipamento, text="Cadastro de Equipamento", font=("Arial", 16, "bold")).grid(row=1, column=0, pady=(0, 15))
    
    tk.Label(frame_cadastro_equipamento, text="Nome do Equipamento:", font=("Arial", 15, "bold")).grid(row=2, column=0, pady=(0, 5))
    ent_nome_equipamento = tk.Entry(frame_cadastro_equipamento, width=40)
    ent_nome_equipamento.grid(row=3, column=0, pady=(0, 10))

    tk.Label(frame_cadastro_equipamento, text="Quantidade Disponível:", font=("Arial", 15, "bold")).grid(row=4, column=0, pady=(0, 5))
    ent_quantidade = tk.Entry(frame_cadastro_equipamento, width=40)
    ent_quantidade.grid(row=5, column=0, pady=(0, 10))

    def salvar_equipamento():
        nome = ent_nome_equipamento.get()
        quantidade_disponivel = ent_quantidade.get()

        if nome == "" or quantidade_disponivel == "":
            messagebox.showwarning("Atencao", "Preencha pelo menos o Nome e a Quantidade do Equipamento.")
            return

        cadastro_equipamento = bd.cadastrar_equipamento(
            nome, quantidade_disponivel)

        if cadastro_equipamento:
            messagebox.showinfo("Sucesso", "Equipamento cadastrado!")
        else:
            messagebox.showerror("Erro", "Ja existe um equipamento cadastrado.")

    def deletar_equipamento():
        item_selecionado = tabela.selection()

        valores = tabela.item(item_selecionado, "values")
        id_equipamento = valores[0]

        if messagebox.askyesno("Confirmar", "Deseja excluir este equipamento?"):
            bd.deletar_equipamento(id_equipamento)

    #Esperando o command para editar e excluir o registro do equipamento
    tk.Button(frame_cadastro_equipamento, text="Salvar", command=salvar_equipamento, bg="#1f4fc4", fg="white").grid(row=6, column=0, pady=(0, 15))
    tk.Button(frame_cadastro_equipamento, text="Editar", bg="#1f4fc4", fg="white").grid(row=7, column=0, pady=(0, 15))
    tk.Button(frame_cadastro_equipamento, text="Excluir", command=deletar_equipamento ,bg="#d32d2d", fg="black").grid(row=8, column=0, pady=(0, 15))

    frame_tabela_equipamento = tk.Frame(container)
    frame_tabela_equipamento.grid(row=10, column=0, pady=15, padx=20, sticky="nsew")

    colunas = ("id", "equipamento", "quantidade")

    tabela = ttk.Treeview(
        frame_tabela_equipamento,
        columns=colunas,
        show="headings",
        height=7
    )

    # Cabeçalhos
    tabela.heading("id", text="Id")
    tabela.heading("equipamento", text="Nome do Equipamento")
    tabela.heading("quantidade", text="Quantidade Disponível")

    # Tamanho das colunas
    tabela.column("id", width=50, anchor="center")
    tabela.column("equipamento", width=100, anchor="center")
    tabela.column("quantidade", width=20, anchor="center")

    # Scrollbar vertical
    scroll_y = ttk.Scrollbar(
        frame_tabela_equipamento,
        orient="vertical",
        command=tabela.yview
    )

    tabela.configure(yscrollcommand=scroll_y.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")

    # Permite a tabela expandir dentro do frame
    frame_tabela_equipamento.grid_rowconfigure(0, weight=1)
    frame_tabela_equipamento.grid_columnconfigure(0, weight=1)

    # --- CARREGAR DADOS NA TABELA ---
    equipamentos = bd.listar_equipamentos()

    for linha in equipamentos:
        tabela.insert("", "end", values=linha)






