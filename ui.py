# ============================================================
# UI.PY - SISTEMA DE DESIGN DO SHARESPACE
# Redesign profissional feito em 23/06/2026
# ------------------------------------------------------------
# Este arquivo e o "kit de pecas visuais" do sistema. Em vez de
# cada tela escolher cores e fontes do seu jeito, todas usam o
# que esta definido aqui. Assim o visual fica IGUAL e PROFISSIONAL
# em todo lugar, e se voce quiser mudar uma cor, muda so aqui.
#
# Tem 3 partes:
#   1) PALETA (cores) e FONTES
#   2) ICONES desenhados com a biblioteca Pillow (PIL)
#   3) PECAS prontas: botoes, cards, campos, tabelas...
# ============================================================

import math
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk, ImageColor

# ------------------------------------------------------------
# 1) PALETA DE CORES (estilo painel moderno, tema claro)
# ------------------------------------------------------------
COR_FUNDO        = "#eef2f7"   # fundo geral da janela (cinza bem claro)
COR_CARD         = "#ffffff"   # fundo dos cartoes (branco)
COR_PRIMARIA     = "#2563eb"   # azul da marca (botoes, destaques)
COR_PRIM_HOVER   = "#1d4ed8"   # azul mais escuro (quando passa o mouse)
COR_PRIM_CLARA   = "#dbeafe"   # azul bem claro (fundos suaves)
COR_TEXTO        = "#0f172a"   # texto principal (quase preto)
COR_TEXTO_FRACO  = "#64748b"   # texto secundario (cinza)
COR_BORDA        = "#e2e8f0"   # linhas e bordas finas
COR_SUCESSO      = "#16a34a"   # verde
COR_SUCESSO_HV   = "#15803d"
COR_PERIGO       = "#dc2626"   # vermelho
COR_PERIGO_HV    = "#b91c1c"
COR_AVISO        = "#d97706"   # laranja
COR_NEUTRO       = "#e2e8f0"   # botao neutro (fundo)
COR_NEUTRO_HV    = "#cbd5e1"
COR_ZEBRA        = "#f8fafc"   # cor das linhas pares da tabela

# ------------------------------------------------------------
# FONTES (Segoe UI = fonte moderna padrao do Windows)
# ------------------------------------------------------------
FONTE   = "Segoe UI"
F_LOGO  = (FONTE, 22, "bold")
F_H1    = (FONTE, 24, "bold")
F_H2    = (FONTE, 16, "bold")
F_LABEL = (FONTE, 10, "bold")
F_TEXTO = (FONTE, 11)
F_PEQ   = (FONTE, 9)
F_BOTAO = (FONTE, 11, "bold")
F_NUM   = (FONTE, 26, "bold")


# ============================================================
# 2) ICONES DESENHADOS COM PILLOW
# ------------------------------------------------------------
# Como o Tk 8.6 nao mostra emojis coloridos, a gente DESENHA cada
# icone com linhas e formas. Desenhamos grande (4x) e reduzimos
# depois, pra borda ficar lisinha (isso se chama "antialiasing").
# ============================================================

_S = 4                  # fator de ampliacao (desenha grande, reduz depois)
_cache_icone = {}       # guarda os icones ja desenhados (nao desenhar 2x)


def _rgba(cor):
    # ImageColor entende tanto "#2563eb" quanto nomes como "white".
    r, g, b = ImageColor.getrgb(cor)[:3]
    return (r, g, b, 255)


def _reta(d, x1, y1, x2, y2, cor, w):
    """Desenha uma linha com as pontas arredondadas (fica mais bonito)."""
    d.line((x1, y1, x2, y2), fill=cor, width=w)
    r = w / 2
    d.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=cor)
    d.ellipse((x2 - r, y2 - r, x2 + r, y2 + r), fill=cor)


def icone(nome, tam=22, cor=COR_PRIMARIA):
    """Devolve um icone (imagem) pronto pra usar em Label/Button."""
    chave = (nome, tam, cor)
    if chave in _cache_icone:
        return _cache_icone[chave]

    W = tam * _S
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = _rgba(cor)
    s = max(4, int(W * 0.08))     # espessura do traco
    p = int(W * 0.16)             # margem interna
    cx = cy = W / 2

    if nome == "busca":                       # lupa
        b = (p, p, int(W * 0.62), int(W * 0.62))
        d.ellipse(b, outline=c, width=s)
        _reta(d, int(W * 0.57), int(W * 0.57), W - p, W - p, c, s)

    elif nome == "cliente":                    # pessoa
        hr = W * 0.15
        d.ellipse((cx - hr, p, cx + hr, p + 2 * hr), outline=c, width=s)
        d.arc((p, int(W * 0.52), W - p, int(W * 1.18)), 180, 360, fill=c, width=s)

    elif nome == "sala":                       # porta
        d.rounded_rectangle((p, int(W * 0.12), W - p, W - int(p * 0.5)),
                            radius=W * 0.06, outline=c, width=s)
        kr = W * 0.045
        d.ellipse((W - int(W * 0.34) - kr, cy - kr,
                   W - int(W * 0.34) + kr, cy + kr), fill=c)

    elif nome == "equipamento":                # monitor
        d.rounded_rectangle((p, p, W - p, int(W * 0.64)),
                            radius=W * 0.05, outline=c, width=s)
        _reta(d, cx, int(W * 0.64), cx, int(W * 0.8), c, s)
        _reta(d, int(W * 0.34), int(W * 0.84), int(W * 0.66), int(W * 0.84), c, s)

    elif nome == "historico":                  # relogio
        d.ellipse((p, p, W - p, W - p), outline=c, width=s)
        _reta(d, cx, cy, cx, int(W * 0.3), c, s)
        _reta(d, cx, cy, int(W * 0.66), cy, c, s)

    elif nome == "backup":                     # disquete (salvar)
        d.rounded_rectangle((p, p, W - p, W - p), radius=W * 0.06, outline=c, width=s)
        d.rectangle((int(W * 0.34), p, int(W * 0.66), int(W * 0.32)),
                    outline=c, width=int(s * 0.7))
        d.rounded_rectangle((int(W * 0.3), int(W * 0.52), int(W * 0.7), W - int(p * 1.1)),
                            radius=W * 0.03, outline=c, width=int(s * 0.7))

    elif nome == "config":                     # engrenagem
        R = W * 0.26
        for k in range(8):
            a = math.radians(k * 45)
            _reta(d, cx + math.cos(a) * R, cy + math.sin(a) * R,
                  cx + math.cos(a) * R * 1.45, cy + math.sin(a) * R * 1.45, c, s)
        d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=c, width=s)
        d.ellipse((cx - R * 0.35, cy - R * 0.35, cx + R * 0.35, cy + R * 0.35), fill=c)

    elif nome == "agendamento":                # calendario
        d.rounded_rectangle((p, int(W * 0.2), W - p, W - p),
                            radius=W * 0.05, outline=c, width=s)
        _reta(d, p, int(W * 0.36), W - p, int(W * 0.36), c, s)
        _reta(d, int(W * 0.34), int(W * 0.1), int(W * 0.34), int(W * 0.27), c, s)
        _reta(d, int(W * 0.66), int(W * 0.1), int(W * 0.66), int(W * 0.27), c, s)
        d.ellipse((cx - W * 0.05, int(W * 0.52), cx + W * 0.05, int(W * 0.62)), fill=c)

    elif nome == "sair":                       # logout (porta + seta)
        d.rounded_rectangle((p, p, int(W * 0.5), W - p),
                            radius=W * 0.05, outline=c, width=s)
        _reta(d, int(W * 0.42), cy, W - p, cy, c, s)
        _reta(d, W - p, cy, int(W * 0.78), int(W * 0.33), c, s)
        _reta(d, W - p, cy, int(W * 0.78), int(W * 0.67), c, s)

    elif nome == "voltar":                     # seta (chevron) para a esquerda
        _reta(d, int(W * 0.62), p, int(W * 0.36), cy, c, s)
        _reta(d, int(W * 0.36), cy, int(W * 0.62), W - p, c, s)

    elif nome == "email":                      # envelope
        d.rounded_rectangle((p, int(W * 0.24), W - p, int(W * 0.76)),
                            radius=W * 0.04, outline=c, width=s)
        _reta(d, p + s, int(W * 0.28), cx, int(W * 0.54), c, s)
        _reta(d, cx, int(W * 0.54), W - p - s, int(W * 0.28), c, s)

    elif nome == "senha":                      # cadeado
        d.rounded_rectangle((int(W * 0.26), int(W * 0.46), int(W * 0.74), W - p),
                            radius=W * 0.07, outline=c, width=s)
        d.arc((int(W * 0.34), int(W * 0.2), int(W * 0.66), int(W * 0.6)),
              180, 360, fill=c, width=s)
        d.ellipse((cx - W * 0.04, int(W * 0.6), cx + W * 0.04, int(W * 0.68)), fill=c)

    elif nome == "ocupacao":                   # anel de progresso
        d.arc((p, p, W - p, W - p), -90, 150, fill=c, width=int(s * 1.4))

    elif nome == "disponivel":                 # circulo com check
        d.ellipse((p, p, W - p, W - p), outline=c, width=s)
        _reta(d, int(W * 0.32), cy, int(W * 0.45), int(W * 0.62), c, s)
        _reta(d, int(W * 0.45), int(W * 0.62), int(W * 0.7), int(W * 0.37), c, s)

    elif nome == "manutencao":                 # chave de boca
        _reta(d, int(W * 0.32), int(W * 0.68), int(W * 0.7), int(W * 0.3), c, int(s * 1.6))
        d.ellipse((int(W * 0.18), int(W * 0.18), int(W * 0.42), int(W * 0.42)),
                  outline=c, width=s)

    img = img.resize((tam, tam), Image.LANCZOS)
    foto = ImageTk.PhotoImage(img)
    _cache_icone[chave] = foto
    return foto


def logo(tam=56):
    """Logo do app: quadrado azul com dois quadrados brancos (ideia de 'compartilhar')."""
    chave = ("__logo__", tam)
    if chave in _cache_icone:
        return _cache_icone[chave]
    W = tam * _S
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, W - 1, W - 1), radius=W * 0.24, fill=_rgba(COR_PRIMARIA))
    branco = (255, 255, 255, 255)
    d.rounded_rectangle((int(W * 0.22), int(W * 0.22), int(W * 0.56), int(W * 0.56)),
                        radius=W * 0.06, fill=branco)
    d.rounded_rectangle((int(W * 0.44), int(W * 0.44), int(W * 0.78), int(W * 0.78)),
                        radius=W * 0.06, outline=branco, width=int(W * 0.05))
    d.rounded_rectangle((int(W * 0.44), int(W * 0.44), int(W * 0.78), int(W * 0.78)),
                        radius=W * 0.06, fill=_rgba(COR_PRIMARIA))
    d.rounded_rectangle((int(W * 0.44), int(W * 0.44), int(W * 0.78), int(W * 0.78)),
                        radius=W * 0.06, outline=branco, width=int(W * 0.05))
    img = img.resize((tam, tam), Image.LANCZOS)
    foto = ImageTk.PhotoImage(img)
    _cache_icone[chave] = foto
    return foto


# ============================================================
# 3) TEMA E PECAS PRONTAS
# ============================================================

def aplicar_tema(janela):
    """Configura cores e estilo das tabelas/campos. Chamar 1x no main.py."""
    janela.configure(bg=COR_FUNDO)
    janela.option_add("*Font", (FONTE, 10))

    st = ttk.Style(janela)
    st.theme_use("clam")   # tema que aceita personalizar cores

    # ---- Tabela (Treeview) ----
    st.configure("Treeview",
                 background=COR_CARD, fieldbackground=COR_CARD,
                 foreground=COR_TEXTO, rowheight=32, borderwidth=0,
                 font=(FONTE, 10))
    st.configure("Treeview.Heading",
                 background=COR_PRIMARIA, foreground="white",
                 font=(FONTE, 10, "bold"), relief="flat", padding=8)
    st.map("Treeview.Heading", background=[("active", COR_PRIM_HOVER)])
    st.map("Treeview",
           background=[("selected", COR_PRIM_CLARA)],
           foreground=[("selected", COR_TEXTO)])

    # ---- Campos de texto e listas ----
    st.configure("TEntry", fieldbackground="white", bordercolor=COR_BORDA,
                 lightcolor=COR_BORDA, darkcolor=COR_BORDA, padding=6)
    st.configure("TCombobox", fieldbackground="white", bordercolor=COR_BORDA,
                 arrowcolor=COR_PRIMARIA, padding=6)

    # ---- Barra de rolagem discreta ----
    st.configure("Vertical.TScrollbar", background=COR_NEUTRO,
                 troughcolor=COR_FUNDO, bordercolor=COR_FUNDO,
                 arrowcolor=COR_TEXTO_FRACO)


def limpar(container):
    """Apaga a tela anterior e pinta o fundo. Toda tela comeca chamando isto."""
    for w in container.winfo_children():
        w.destroy()
    container.configure(bg=COR_FUNDO)


def lbl(parent, texto, fonte=F_TEXTO, fg=COR_TEXTO, bg=COR_CARD, **kw):
    return tk.Label(parent, text=texto, font=fonte, fg=fg, bg=bg, **kw)


def card(parent, bg=COR_CARD):
    """Um cartao branco com borda fina (a 'caixa' do visual moderno)."""
    return tk.Frame(parent, bg=bg, highlightbackground=COR_BORDA,
                    highlightthickness=1, bd=0)


_VARIANTES = {
    "primario": (COR_PRIMARIA, "white", COR_PRIM_HOVER),
    "sucesso":  (COR_SUCESSO,  "white", COR_SUCESSO_HV),
    "perigo":   (COR_PERIGO,   "white", COR_PERIGO_HV),
    "neutro":   (COR_NEUTRO,   COR_TEXTO, COR_NEUTRO_HV),
}


def botao(parent, texto, comando, variante="primario", icone_nome=None, largo=False):
    """Botao 'flat' moderno, com efeito ao passar o mouse (hover)."""
    bg, fg, bg_hv = _VARIANTES[variante]
    b = tk.Button(parent, text=("  " + texto if icone_nome else texto),
                  command=comando, bg=bg, fg=fg,
                  activebackground=bg_hv, activeforeground=fg,
                  font=F_BOTAO, relief="flat", bd=0, cursor="hand2",
                  padx=18, pady=10)
    if icone_nome:
        img = icone(icone_nome, 18, fg)
        b.config(image=img, compound="left")
        b.image = img
    if largo:
        b.config(width=1)   # deixa o sticky/fill controlar a largura
    b.bind("<Enter>", lambda e: b.config(bg=bg_hv))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


def botao_link(parent, texto, comando):
    """Botao discreto, parece um link (sem fundo)."""
    b = tk.Button(parent, text=texto, command=comando, bg=COR_CARD,
                  fg=COR_PRIMARIA, activebackground=COR_CARD,
                  activeforeground=COR_PRIM_HOVER, font=(FONTE, 10, "bold"),
                  relief="flat", bd=0, cursor="hand2")
    return b


def barra_topo(container, titulo, comando_voltar=None):
    """Cabecalho da tela: (botao voltar) + titulo. Devolve a area de conteudo."""
    topo = tk.Frame(container, bg=COR_FUNDO)
    topo.pack(fill="x", padx=24, pady=(18, 6))
    if comando_voltar is not None:
        botao(topo, "Voltar", comando_voltar, variante="neutro",
              icone_nome="voltar").pack(side="left")
    lbl(topo, titulo, fonte=F_H1, bg=COR_FUNDO).pack(side="left", padx=16)
    # area onde a tela coloca o conteudo dela
    corpo = tk.Frame(container, bg=COR_FUNDO)
    corpo.pack(fill="both", expand=True, padx=24, pady=12)
    return corpo


def campo(parent, rotulo, show=None, valores=None, largura=34):
    """Cria um rotulo + uma caixa de digitar (ou de escolher). Devolve a caixa."""
    lbl(parent, rotulo, fonte=F_LABEL, fg=COR_TEXTO_FRACO,
        bg=parent["bg"]).pack(anchor="w", pady=(10, 2))
    if valores is not None:
        ent = ttk.Combobox(parent, values=valores, width=largura, font=F_TEXTO)
    else:
        ent = ttk.Entry(parent, width=largura, font=F_TEXTO)
        if show:
            ent.config(show=show)
    ent.pack(fill="x", ipady=4)
    return ent


def card_menu(parent, icone_nome, titulo, comando):
    """Cartao clicavel do dashboard (icone grande + titulo)."""
    c = tk.Frame(parent, bg=COR_CARD, highlightbackground=COR_BORDA,
                 highlightthickness=1, cursor="hand2")
    bolha = tk.Frame(c, bg=COR_PRIM_CLARA, width=56, height=56)
    bolha.pack(pady=(22, 10))
    bolha.pack_propagate(False)
    ic = icone(icone_nome, 28, COR_PRIMARIA)
    li = tk.Label(bolha, image=ic, bg=COR_PRIM_CLARA)
    li.image = ic
    li.place(relx=0.5, rely=0.5, anchor="center")
    lt = lbl(c, titulo, fonte=F_H2)
    lt.pack(pady=(0, 22), padx=14)

    def entra(_=None):
        c.config(highlightbackground=COR_PRIMARIA, highlightthickness=2)

    def sai(_=None):
        c.config(highlightbackground=COR_BORDA, highlightthickness=1)

    for w in (c, bolha, li, lt):
        w.bind("<Enter>", entra)
        w.bind("<Leave>", sai)
        w.bind("<Button-1>", lambda e: comando())
    return c


def card_estatistica(parent, icone_nome, cor_icone, valor, descricao):
    """Cartao de numero do dashboard (icone + numero grande + texto)."""
    c = card(parent)
    linha = tk.Frame(c, bg=COR_CARD)
    linha.pack(fill="x", padx=18, pady=18)
    ic = icone(icone_nome, 34, cor_icone)
    li = tk.Label(linha, image=ic, bg=COR_CARD)
    li.image = ic
    li.pack(side="left", padx=(0, 14))
    txt = tk.Frame(linha, bg=COR_CARD)
    txt.pack(side="left", anchor="w")
    lbl(txt, valor, fonte=F_NUM).pack(anchor="w")
    lbl(txt, descricao, fonte=F_PEQ, fg=COR_TEXTO_FRACO).pack(anchor="w")
    return c


def zebrar(tabela, linhas):
    """Preenche a tabela alternando a cor das linhas (efeito 'zebra')."""
    tabela.tag_configure("par", background=COR_ZEBRA)
    tabela.tag_configure("impar", background=COR_CARD)
    for i, linha in enumerate(linhas):
        tag = "par" if i % 2 == 0 else "impar"
        tabela.insert("", "end", values=linha, tags=(tag,))
