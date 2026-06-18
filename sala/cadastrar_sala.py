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
def montar_cadastrar_sala(container, funcao_voltar):
    for widget in container.winfo_children():
        widget.destroy()

    container.grid_columnconfigure(0, weight=1)

# --- BOTÃO VOLTAR ---
    # Ele fica no topo para fácil acesso
    tk.Button(container, text="← Voltar", command=funcao_voltar, bg="#1f4fc4", fg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    
    frame_cadastro_sala = tk.Frame(container)
    frame_cadastro_sala.grid(row=1, column=0, pady=10)

    tk.Label(frame_cadastro_sala, text="ShareSpace", font=("Arial", 24, "bold")).grid(row=0, column=0, pady=(0, 15))
    tk.Label(frame_cadastro_sala, text="Cadastro de Sala", font=("Arial", 16, "bold")).grid(row=1, column=0, pady=(0, 15))
    
    tk.Label(frame_cadastro_sala, text="Nome da Sala:", font=("Arial", 15, "bold")).grid(row=2, column=0, pady=(0, 5))
    ent_nome_sala = tk.Entry(frame_cadastro_sala, width=40)
    ent_nome_sala.grid(row=3, column=0, pady=(0, 10))

    tk.Label(frame_cadastro_sala, text="Capacidade:", font=("Arial", 15, "bold")).grid(row=4, column=0, pady=(0, 5))
    ent_capacidade = tk.Entry(frame_cadastro_sala, width=40)
    ent_capacidade.grid(row=5, column=0, pady=(0, 10))

    tk.Button(frame_cadastro_sala, text="Salvar", bg="#1f4fc4", fg="white").grid(row=6, column=0, pady=(0, 15))




