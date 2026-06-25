# ============================================================
# TELA DE BUSCA DE SALAS  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Lista as salas REAIS do banco, agrupadas por situacao:
#   - DISPONIVEIS
#   - OCUPADAS / INDISPONIVEIS
#   - EM MANUTENCAO
#
# Modificações feitas por Dener (25/06/2026)
#   - Agora usa os dados REAIS do banco (antes as salas eram fixas no codigo).
#   - FILTRO funcional: escolhe data + horario e mostra quais salas estao livres
#     nesse periodo (usa checar_conflito_reserva). Sem horario, lista por situacao.
#   - Botao MANUTENCAO em cada sala (e "Liberar" para tirar da manutencao).
#   - Botao "Reservar" leva para o agendamento ja com a sala escolhida.
#   - Data por CALENDARIO e horarios por LISTA (igual a tela de agendamento).
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import banco_dados as bd
import ui


def montar_busca_salas(container, navegar):
    ui.limpar(container)
    corpo = ui.barra_topo(container, "Busca de Salas", lambda: navegar("dashboard"))

    # ---- Card de filtros ----
    filtros = ui.card(corpo)
    filtros.pack(fill="x", pady=(0, 10))
    fi = tk.Frame(filtros, bg=ui.COR_CARD)
    fi.pack(fill="x", padx=18, pady=(16, 4))

    # DATA por calendario
    f_data = tk.Frame(fi, bg=ui.COR_CARD)
    f_data.pack(side="left", padx=(0, 18))
    entrada_data = ui.campo_data(f_data, "DATA", largura=12)

    # HORARIOS por lista (podem ficar em branco = sem filtro de horario)
    horarios = [f"{h:02d}:{m:02d}" for h in range(8, 18) for m in (0, 30)] + ["18:00"]
    f_ini = tk.Frame(fi, bg=ui.COR_CARD)
    f_ini.pack(side="left", padx=(0, 18))
    entrada_inicio = ui.campo(f_ini, "HORÁRIO INÍCIO", valores=horarios[:-1], largura=8)
    f_fim = tk.Frame(fi, bg=ui.COR_CARD)
    f_fim.pack(side="left", padx=(0, 18))
    entrada_fim = ui.campo(f_fim, "HORÁRIO FIM", valores=horarios[1:], largura=8)

    # Botoes de acao do filtro
    f_btn = tk.Frame(fi, bg=ui.COR_CARD)
    f_btn.pack(side="left", anchor="s")
    ui.botao(f_btn, "Filtrar", lambda: atualizar_lista(), icone_nome="busca").pack(side="left")
    ui.botao(f_btn, "Limpar", lambda: limpar_filtro(), variante="neutro").pack(side="left", padx=(8, 0))

    ui.lbl(filtros, "Deixe os horários em branco para listar todas as salas pela situação atual.",
           fonte=ui.F_PEQ, fg=ui.COR_TEXTO_FRACO).pack(anchor="w", padx=18, pady=(0, 12))

    # ---- Resultados (com rolagem) ----
    res = tk.Frame(corpo, bg=ui.COR_FUNDO)
    res.pack(fill="both", expand=True, pady=(10, 0))
    canvas = tk.Canvas(res, bg=ui.COR_FUNDO, highlightthickness=0)
    sb = ttk.Scrollbar(res, orient="vertical", command=canvas.yview)
    lista = tk.Frame(canvas, bg=ui.COR_FUNDO)
    lista.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    win = canvas.create_window((0, 0), window=lista, anchor="nw")
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
    canvas.configure(yscrollcommand=sb.set)
    canvas.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    def _roda(e):
        if canvas.winfo_exists():
            canvas.yview_scroll(int(-e.delta / 120), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _roda))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # ------------------------------------------------------------
    # Pecas da listagem
    # ------------------------------------------------------------
    def titulo_grupo(texto, cor):
        cab = tk.Frame(lista, bg=ui.COR_FUNDO)
        cab.pack(fill="x", pady=(14, 4), anchor="w")
        ui.lbl(cab, texto, fonte=ui.F_LABEL, fg=cor, bg=ui.COR_FUNDO).pack(side="left")

    def linha_sala(s, grupo):
        id_sala, nome, numero, andar, capac, obs, status = s
        c = ui.card(lista)
        c.pack(fill="x", pady=4)
        dentro = tk.Frame(c, bg=ui.COR_CARD)
        dentro.pack(fill="x", padx=16, pady=12)

        if grupo == "manutencao":
            ic_nome, cor = "manutencao", ui.COR_PERIGO
        elif grupo == "ocupadas":
            ic_nome, cor = "historico", ui.COR_AVISO
        else:
            ic_nome, cor = "disponivel", ui.COR_SUCESSO

        ic = ui.icone(ic_nome, 20, cor)
        li = tk.Label(dentro, image=ic, bg=ui.COR_CARD)
        li.image = ic
        li.pack(side="left", padx=(0, 10))

        texto = f"{nome} ({numero})   -   {andar}º andar - {capac} lugares"
        ui.lbl(dentro, texto, fonte=ui.F_TEXTO).pack(side="left")

        if status == "manutencao":
            # tirar da manutencao
            ui.botao(dentro, "Liberar", lambda: mudar_status(id_sala, "disponivel"),
                     variante="sucesso", icone_nome="disponivel").pack(side="right", padx=(0, 4))
        else:
            # colocar em manutencao
            ui.botao(dentro, "Manutenção", lambda: mudar_status(id_sala, "manutencao"),
                     variante="neutro", icone_nome="manutencao").pack(side="right", padx=(0, 4))
            # so faz sentido reservar uma sala que esta livre
            if grupo == "disponiveis":
                ui.botao(dentro, "Reservar", lambda n=nome: navegar("agendamento", sala=n),
                         icone_nome="agendamento").pack(side="right", padx=(0, 8))

    # ------------------------------------------------------------
    # Acoes
    # ------------------------------------------------------------
    def mudar_status(id_sala, novo_status):
        bd.atualizar_status_sala(id_sala, novo_status)
        atualizar_lista()   # redesenha ja com a situacao nova

    def limpar_filtro():
        entrada_inicio.set("")
        entrada_fim.set("")
        atualizar_lista()

    def atualizar_lista():
        for w in lista.winfo_children():
            w.destroy()

        salas = bd.listar_salas()
        if not salas:
            ui.lbl(lista, "Nenhuma sala cadastrada ainda. Cadastre no menu 'Cadastrar Sala'.",
                   fonte=ui.F_TEXTO, fg=ui.COR_TEXTO_FRACO, bg=ui.COR_FUNDO).pack(anchor="w", pady=20)
            return

        data = entrada_data.get().strip()
        inicio = entrada_inicio.get().strip()
        fim = entrada_fim.get().strip()
        usar_horario = bool(inicio and fim)
        if usar_horario and inicio >= fim:
            messagebox.showwarning("Atenção", "O horário de início deve ser anterior ao fim.")
            usar_horario = False

        # Separa as salas em 3 grupos
        grupos = {"disponiveis": [], "ocupadas": [], "manutencao": []}
        for s in salas:
            status = s[6]
            if status == "manutencao":
                grupos["manutencao"].append(s)
            elif status == "indisponivel":
                grupos["ocupadas"].append(s)
            else:  # 'disponivel'
                # se filtrou por horario, verifica se ha reserva no periodo
                if usar_horario and bd.checar_conflito_reserva(s[0], data, inicio, fim):
                    grupos["ocupadas"].append(s)
                else:
                    grupos["disponiveis"].append(s)

        titulo_disp = (f"DISPONÍVEIS EM {data} DAS {inicio} ÀS {fim}"
                       if usar_horario else "DISPONÍVEIS")
        secoes = [
            (titulo_disp,                  ui.COR_SUCESSO, "disponiveis"),
            ("OCUPADAS / INDISPONÍVEIS",   ui.COR_AVISO,   "ocupadas"),
            ("EM MANUTENÇÃO",              ui.COR_PERIGO,  "manutencao"),
        ]
        for titulo, cor, chave in secoes:
            titulo_grupo(titulo, cor)
            if grupos[chave]:
                for s in grupos[chave]:
                    linha_sala(s, chave)
            else:
                ui.lbl(lista, "   (nenhuma)", fonte=ui.F_PEQ, fg=ui.COR_TEXTO_FRACO,
                       bg=ui.COR_FUNDO).pack(anchor="w")

    # Primeira carga: mostra todas as salas pela situacao atual.
    atualizar_lista()
