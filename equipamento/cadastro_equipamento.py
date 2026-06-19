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
            navegar("dashboard")
        else:
            messagebox.showerror("Erro", "Ja existe um equipamento cadastrado.")

    #Esperando o command para editar e excluir o registro do equipamento
    tk.Button(frame_cadastro_equipamento, text="Salvar", command=salvar_equipamento, bg="#1f4fc4", fg="white").grid(row=6, column=0, pady=(0, 15))
    tk.Button(frame_cadastro_equipamento, text="Editar", bg="#1f4fc4", fg="white").grid(row=7, column=0, pady=(0, 15))
    tk.Button(frame_cadastro_equipamento, text="Excluir", bg="#d32d2d", fg="black").grid(row=8, column=0, pady=(0, 15))






