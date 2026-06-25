# ============================================================
# TELA DE BUSCA DE SALAS  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Card de filtros no topo + lista de resultados com etiquetas
# coloridas (verde = disponivel, laranja = ocupada, vermelho =
# manutencao).
# Modificado por Fernando (23/06/2026) - Ajustes de ortografia e layout.
# Modificações feitas por Fernando (25/06/2026)
#   - Adicionado o aplicar_mascara para data e horario, evitando que o usuario digite algo invalido..
#   - Adicionado a função de filtrar resultados (ainda sem logica, apenas mockup).
#   - Modificação na def linha_sala para adicionar o botão de reservar, que leva para a tela de agendamento.
#   - Adicionado a função carregar_todas_as_salas, que mostra a situação atual das salas no banco de dados/sistema.
# ============================================================

import tkinter as tk
from tkinter import ttk
import ui

def aplicar_mascara(event, entry, formato):
    texto_raw = "".join(filter(str.isdigit, entry.get()))
    
    # 1. Validação de DATA (Formato AAAA-MM-DD)
    if formato == "####-##-##" and len(texto_raw) >= 6:
        mes = int(texto_raw[4:6])
        if mes > 12: texto_raw = texto_raw[:4] + "12" + texto_raw[6:]
        if mes == 0: texto_raw = texto_raw[:4] + "01" + texto_raw[6:]
        
        if len(texto_raw) >= 8:
            dia = int(texto_raw[6:8])
            # Trava básica de dia em 31
            if dia > 31: texto_raw = texto_raw[:6] + "31"
            if dia == 0: texto_raw = texto_raw[:6] + "01"

    # 2. Validação de HORÁRIO (Formato ##:##)
    elif formato == "##:##" and len(texto_raw) >= 2:
        horas = int(texto_raw[:2])
        if horas > 23: texto_raw = "23" + texto_raw[2:]
        if len(texto_raw) >= 4:
            minutos = int(texto_raw[2:4])
            if minutos > 59: texto_raw = texto_raw[:2] + "59"

    # Montagem final do texto com o formato
    novo_texto = ""
    i = 0
    for char in formato:
        if i >= len(texto_raw): break
        if char == "#":
            novo_texto += texto_raw[i]
            i += 1
        else:
            novo_texto += char
    
    entry.delete(0, tk.END)
    entry.insert(0, novo_texto)

def montar_busca_salas(container, navegar):
    ui.limpar(container)
    corpo = ui.barra_topo(container, "Busca de Salas", lambda: navegar("dashboard"))

    # ---- Card de filtros ----
    filtros = ui.card(corpo)
    filtros.pack(fill="x", pady=(0, 10))
    fi = tk.Frame(filtros, bg=ui.COR_CARD)
    fi.pack(fill="x", padx=18, pady=16)

    def campo_inline(rotulo, largura, formato=None):
        f = tk.Frame(fi, bg=ui.COR_CARD)
        ui.lbl(f, rotulo, fonte=ui.F_LABEL, fg=ui.COR_TEXTO_FRACO).pack(anchor="w", pady=(0, 2))
        
        e = ttk.Entry(f, width=largura, font=ui.F_TEXTO, justify="center")
        e.pack(ipady=4, fill="x")
        
        if formato:
            # Vincula o evento de soltar tecla à função de máscara
            e.bind("<KeyRelease>", lambda event, entry=e, f=formato: aplicar_mascara(event, entry, f))
        
        return f, e

    # DATA (AAAA-MM-DD)
    f1, entry_data = campo_inline("DATA DA RESERVA", 16, formato="####-##-##")
    f1.pack(side="left", padx=(0, 18))

    # HORÁRIO INÍCIO
    f2, entry_inicio = campo_inline("HORÁRIO INÍCIO", 10, formato="##:##")
    f2.pack(side="left", padx=(0, 18))

    # HORÁRIO FIM
    f3, entry_fim = campo_inline("HORÁRIO FIM", 10, formato="##:##")
    f3.pack(side="left", padx=(0, 18))

    # Botão de buscar estilizado
    btn_buscar = ui.botao(fi, "Filtrar Salas", lambda: filtrar_resultados(), 
                           variante="primario", icone_nome="busca")
    btn_buscar.pack(side="left", anchor="s", padx=(6, 0))

    # ---- Resultados ----
    res = tk.Frame(corpo, bg=ui.COR_FUNDO)
    res.pack(fill="both", expand=True, pady=(10, 0))

    def titulo_grupo(texto, cor):
        cab = tk.Frame(res, bg=ui.COR_FUNDO)
        cab.pack(fill="x", pady=(14, 4), anchor="w")
        ui.lbl(cab, texto, fonte=ui.F_LABEL, fg=cor, bg=ui.COR_FUNDO).pack(side="left")

    def linha_sala(texto, com_botao=False, icone_nome="disponivel", cor_icone=ui.COR_SUCESSO):
        c = ui.card(res)
        c.pack(fill="x", pady=4)
        
        dentro = tk.Frame(c, bg=ui.COR_CARD)
        dentro.pack(fill="x", padx=16, pady=12)
        
        ic = ui.icone(icone_nome, tam=20, cor=cor_icone)
        li = tk.Label(dentro, image=ic, bg=ui.COR_CARD)
        li.image = ic
        li.pack(side="left", padx=(0, 10))
        
        if " - " in texto:
            nome_sala, detalhes = texto.split(" - ", 1)
            ui.lbl(dentro, nome_sala, fonte=ui.F_LABEL).pack(side="left")
            ui.lbl(dentro, f"  -  {detalhes}", fonte=ui.F_TEXTO).pack(side="left")
        else:
            ui.lbl(dentro, texto, fonte=ui.F_TEXTO).pack(side="left")
        
        if com_botao:
            ui.botao(dentro, "Reservar", lambda s=nome_sala: navegar("agendamento", sala=s), 
            icone_nome="agendamento").pack(side="right", padx=(0, 4))

    def carregar_todas_as_salas():
        # Limpa listagem anterior se houver
        for widget in res.winfo_children():
            widget.destroy()
            
        # Exibe imediatamente a situação atual do banco de dados/sistema
        titulo_grupo("DISPONÍVEIS", ui.COR_SUCESSO)
        linha_sala("Sala Alfa  - 1º andar - 8 lugares", com_botao=True, icone_nome="disponivel", cor_icone=ui.COR_SUCESSO)
        linha_sala("Sala Delta  - 2º andar - 4 lugares", com_botao=True, icone_nome="disponivel", cor_icone=ui.COR_SUCESSO)

        titulo_grupo("INDISPONÍVEIS / OCUPADAS", ui.COR_AVISO)
        linha_sala("Sala Beta (502)  - 5º andar - 6 lugares [Ocupada das 14h às 17h]", icone_nome="historico", cor_icone=ui.COR_AVISO)

        titulo_grupo("EM MANUTENÇÃO", ui.COR_PERIGO)
        linha_sala("Sala Gama (1503) - 15º andar - 10 lugares [Em manutenção]", icone_nome="manutencao", cor_icone=ui.COR_PERIGO)

    def filtrar_resultados():
        carregar_todas_as_salas()

    carregar_todas_as_salas()

 
