# ============================================================
# TELA DE BUSCA DE SALAS  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Card de filtros no topo + lista de resultados com etiquetas
# coloridas (verde = disponivel, laranja = ocupada, vermelho =
# manutencao).
# Modificado por Fernando (23/06/2026) - Ajustes de ortografia e layout.
# ============================================================

import tkinter as tk
from tkinter import ttk
import ui


def montar_busca_salas(container, navegar):
    ui.limpar(container)
    corpo = ui.barra_topo(container, "Busca de Salas", lambda: navegar("dashboard"))

    # ---- Card de filtros ----
    filtros = ui.card(corpo)
    filtros.pack(fill="x")
    fi = tk.Frame(filtros, bg=ui.COR_CARD)
    fi.pack(fill="x", padx=18, pady=16)

    def campo_inline(rotulo, largura):
        f = tk.Frame(fi, bg=ui.COR_CARD)
        ui.lbl(f, rotulo, fonte=ui.F_LABEL, fg=ui.COR_TEXTO_FRACO).pack(anchor="w")
        e = ttk.Entry(f, width=largura, font=ui.F_TEXTO)
        e.pack(ipady=3)
        return f, e

    f1, _ = campo_inline("DATA (AAAA-MM-DD)", 14)
    f1.pack(side="left", padx=(0, 14))
    f2, _ = campo_inline("INÍCIO", 8)
    f2.pack(side="left", padx=(0, 14))
    f3, _ = campo_inline("FIM", 8)
    f3.pack(side="left", padx=(0, 14))
    ui.botao(fi, "BUSCAR", lambda: None, icone_nome="busca").pack(side="left",
                                                                  anchor="s", pady=(0, 1))

    # ---- Resultados ----
    res = tk.Frame(corpo, bg=ui.COR_FUNDO)
    res.pack(fill="both", expand=True, pady=(18, 0))

    def titulo_grupo(texto, cor):
        cab = tk.Frame(res, bg=ui.COR_FUNDO)
        cab.pack(fill="x", pady=(12, 4))
        tk.Frame(cab, bg=cor, width=12, height=12).pack(side="left", pady=4)
        ui.lbl(cab, texto, fonte=ui.F_LABEL, fg=cor, bg=ui.COR_FUNDO).pack(side="left", padx=8)

    def linha_sala(texto, com_botao=False):
        c = ui.card(res)
        c.pack(fill="x", pady=4)
        dentro = tk.Frame(c, bg=ui.COR_CARD)
        dentro.pack(fill="x", padx=16, pady=10)
        ui.lbl(dentro, texto, fonte=ui.F_TEXTO).pack(side="left")
        if com_botao:
            ui.botao(dentro, "Reservar", lambda: navegar("agendamento"),
                     icone_nome="agendamento").pack(side="right")

    titulo_grupo("DISPONÍVEIS", ui.COR_SUCESSO)
    linha_sala("Sala Alfa  - 1º andar - 8 lugares", com_botao=True)

    titulo_grupo("INDISPONÍVEIS", ui.COR_AVISO)
    linha_sala("Sala Beta (502)  - 5º andar - 6 lugares [Ocupada das 14h às 17h]")

    titulo_grupo("EM MANUTENÇÃO", ui.COR_PERIGO)
    linha_sala("Sala Gama (1503) - 15º andar - 10 lugares [Em manutenção]")
