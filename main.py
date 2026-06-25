# ============================================================
# MAIN.PY - O "CHEFE" DO PROGRAMA
# Arquivo organizado por Dener em 17/06/2026
# ------------------------------------------------------------
# Este arquivo:
#   1) cria a janela principal do programa;
#   2) prepara o banco de dados (cria as tabelas se ainda nao existirem);
#   3) controla a NAVEGACAO, ou seja, a troca de uma tela pela outra.
#
# Ideia importante: existe UMA janela so. Dentro dela tem uma caixa
# chamada "container". Cada tela e desenhada DENTRO dessa caixa.
# Quando trocamos de tela, a gente limpa a caixa e desenha a nova.
# Kael: Adicionando a tela do cadastro de equipamento 
# Modificado por Fernando (23/06/2026) - Ajustes de ortografia e layout.
# Modificado por Fernando (25/06/2026) - Adicionado o KWARGS para passar a sala selecionada na tela de busca para a tela de agendamento, sem precisar de diversas variaveis.
# ============================================================

import tkinter as tk
import banco_dados as bd
import ui   # sistema de design (cores, fontes, icones, pecas prontas)

# Aqui trazemos a funcao que desenha cada tela. Cada tela mora no seu arquivo.
from login import montar_login
from recuperar_senha import montar_recuperar_senha
from dashboard import montar_dashboard
from cliente.cadastro_cliente import montar_cadastro_cliente
from busca_salas import montar_busca_salas
# A tela de agendamento fica dentro da pasta "reserva".
from reserva.agendamento import montar_agendamento
from historico import montar_historico
from backup import montar_backup
# A tela de cadastro de sala fica dentro da pasta "sala".
from sala.cadastrar_sala import montar_cadastrar_sala
from equipamento.cadastro_equipamento import montar_cadastro_equipamento


# Cria o banco e as tabelas caso seja a primeira vez que o programa roda.
bd.inicializar_banco()

# ---- Janela principal ----
janela = tk.Tk()
janela.title("ShareSpace - Gestão de Salas de Reunião")

# Aplica o tema profissional (cores, fontes, estilo das tabelas).
ui.aplicar_tema(janela)

janela.geometry("1100x700")   # tamanho de RESTAURACAO (ao sair do maximizado)
janela.minsize(900, 600)      # nao deixa encolher demais e quebrar o layout
janela.state("zoomed")        # abre MAXIMIZADO, encaixado na tela do usuario

# A "caixa" onde todas as telas vao aparecer.
container = tk.Frame(janela, bg=ui.COR_FUNDO)
container.pack(fill="both", expand=True)


# ---- A funcao mais importante: trocar de tela ----
# Para mudar de tela, em qualquer lugar do programa, basta chamar:
#   navegar("dashboard")  ->  abre o dashboard
#   navegar("login")      ->  abre o login
# E por ai vai. O nome dentro das aspas decide qual tela abrir.
def navegar(nome_tela, **kwargs):
    if nome_tela == "login":
        montar_login(container, navegar)
    elif nome_tela == "recuperar_senha":
        montar_recuperar_senha(container, navegar)
    elif nome_tela == "dashboard":
        montar_dashboard(container, navegar)
    elif nome_tela == "cadastro_sala":
         # A tela de sala usa "funcao_voltar" (uma funcao sem nada dentro dos parenteses).
        # Por isso passamos um lambda que volta para o dashboard.
        montar_cadastrar_sala(container, lambda: navegar("dashboard"))
    elif nome_tela == "cadastro_cliente":
        montar_cadastro_cliente(container, navegar)
    elif nome_tela == "busca":
        montar_busca_salas(container, navegar)
    elif nome_tela == "cadastro_equipamento":
        montar_cadastro_equipamento(container, navegar)
    elif nome_tela == "agendamento":
        # passamos o "sala" que veio do kwargs
        montar_agendamento(container, navegar, sala_selecionada=kwargs.get("sala"))
    elif nome_tela == "historico":
        montar_historico(container, navegar)
    elif nome_tela == "backup":
        montar_backup(container, navegar)


# Comecamos o programa mostrando a tela de login.
navegar("login")

# mainloop() deixa a janela "viva" na tela, esperando os cliques do usuario.
# O programa fica aqui ate a janela ser fechada.
janela.mainloop()
