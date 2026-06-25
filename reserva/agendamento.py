# ============================================================
# TELA DE AGENDAMENTO  (redesign profissional - 23/06/2026)
# ------------------------------------------------------------
# Cartao central com os campos da reserva (sala, cliente, data,
# horarios).
#
# As REGRAS (nao deixar horario repetido, reserva de 30min a 4h,
# so de segunda a sexta das 08h as 18h, sem data no passado) e o
# salvar no banco ficam para a proxima etapa (logica do Kael a ser
# reimplementada neste novo layout).
# Modificações feitas por Fernando (25/06/2026)
#   - Adicionado o datetime para validar as regras de negocio (data no passado, segunda a sexta, horario permitido, duracao da reserva).
#   - Adicionado a função de checar conflito de reserva no banco de dados.
#   - Feita a lógica da função confirmar() para validar os campos e aplicar as regras de negocio.
#   - Adicionado o botão de confirmar agendamento, que chama a função confirmar() e salva no banco de dados.
# ============================================================

import tkinter as tk
from tkinter import messagebox
from datetime import datetime  # << IMPORTAÇÃO ADICIONADA PARA AS REGRAS FUNCIONAREM
import banco_dados as bd
import ui


def montar_agendamento(container, navegar, sala_selecionada=None):
    ui.limpar(container)
    corpo = ui.barra_topo(container, "Novo Agendamento", lambda: navegar("dashboard"))

    # Uso do GRID para garantir que o cartão se ajuste e revele o botão
    corpo.rowconfigure(0, weight=1)
    corpo.columnconfigure(0, weight=1)

    cartao = ui.card(corpo)
    cartao.grid(row=0, column=0, pady=10, padx=10)
    
    interno = tk.Frame(cartao, bg=ui.COR_CARD)
    interno.pack(padx=35, pady=12)

    ui.lbl(interno, "Dados da reserva", fonte=ui.F_H2).pack(anchor="w", pady=(0, 2))

    salas = bd.listar_salas()
    nomes_salas = [s[1] for s in salas]
    caixa_sala = ui.campo(interno, "SALA", valores=nomes_salas)

    if sala_selecionada:
        caixa_sala.set(sala_selecionada)

    clientes = bd.listar_clientes()
    nomes_clientes = [c[2] for c in clientes]
    caixa_cliente = ui.campo(interno, "CLIENTE", valores=nomes_clientes)

    entrada_data = ui.campo(interno, "DATA (AAAA-MM-DD)")
    entrada_inicio = ui.campo(interno, "HORA INICIO (HH:MM)")
    entrada_fim = ui.campo(interno, "HORA FIM (HH:MM)")

    ui.lbl(interno, "MÍNIMO 30MIN, MÁXIMO 4H, SEG A SEX DAS 08H ÀS 18H",
           fonte=ui.F_PEQ, fg=ui.COR_TEXTO_FRACO).pack(anchor="w", pady=(2, 8))

    def confirmar():
        # 1. PEGAR OS DADOS DIGITADOS NA TELA
        sala_nome = caixa_sala.get()
        cliente_nome = caixa_cliente.get()
        data_texto = entrada_data.get().strip()
        inicio_texto = entrada_inicio.get().strip()
        fim_texto = entrada_fim.get().strip()

        # Validação de campos vazios
        if not all([sala_nome, cliente_nome, data_texto, inicio_texto, fim_texto]):
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        # 2. ENCONTRAR O ID DA SALA
        id_sala = None
        for s in salas:
            if s[1] == sala_nome:
                id_sala = int(s[0])
                break

        if id_sala is None:
            messagebox.showerror("Erro", "Sala selecionada inválida.")
            return

        # Encontrar o ID do cliente
        id_cliente = None
        for c in clientes:
            if c[2] == cliente_nome:
                id_cliente = int(c[0])
                break

        if id_cliente is None:
            messagebox.showerror("Erro", "Cliente selecionado inválido.")
            return

        # 3. VALIDAÇÕES DE REGRAS DE NEGÓCIO
        try:
            data_atual = datetime.now()
            data_reserva = datetime.strptime(data_texto, "%Y-%m-%d")
            horario_inicio = datetime.strptime(f"{data_texto} {inicio_texto}", "%Y-%m-%d %H:%M")
            horario_fim = datetime.strptime(f"{data_texto} {fim_texto}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Formato Inválido", "Siga os padrões informados:\nData: AAAA-MM-DD\nHoras: HH:MM")
            return

        # Sem data no passado
        if data_reserva.date() < data_atual.date():
            messagebox.showwarning("Regra de Validação", "Não é permitido agendar em datas passadas.")
            return

        # Apenas de segunda a sexta
        if data_reserva.weekday() > 4:
            messagebox.showwarning("Regra de Validação", "Reservas permitidas apenas de segunda a sexta-feira.")
            return

        # Somente das 08:00 às 18:00
        if horario_inicio.hour < 8 or horario_fim.hour > 18 or (horario_fim.hour == 18 and horario_fim.minute > 0):
            messagebox.showwarning("Regra de Validação", "Horário permitido é estritamente das 08:00 às 18:00.")
            return

        # Início deve ser antes do fim
        if horario_inicio >= horario_fim:
            messagebox.showwarning("Regra de Validação", "O horário de início deve ser anterior ao fim.")
            return

        # Duração da reserva (entre 30 minutos e 4 horas)
        duracao_minutos = (horario_fim - horario_inicio).total_seconds() / 60
        if duracao_minutos < 30:
            messagebox.showwarning("Regra de Validação", "A reserva deve ter no mínimo 30 minutos.")
            return
        if duracao_minutos > 240:
            messagebox.showwarning("Regra de Validação", "A reserva não pode passar de 4 horas.")
            return

        # Não deixar horário repetido (Conflito no Banco)
        if bd.checar_conflito_reserva(id_sala, data_texto, inicio_texto, fim_texto):
            messagebox.showerror("Conflito", "Esta sala já possui uma reserva ativa neste mesmo período!")
            return

        # 4. SALVAR NO BANCO DE DADOS
        try:
            bd.cadastrar_reserva(id_sala, id_cliente, data_texto, inicio_texto, fim_texto, "ativa")
            messagebox.showinfo("Sucesso", "Reserva realizada com sucesso!")
            navegar("dashboard")
        except Exception as erro:
            messagebox.showerror("Erro no Banco", f"Não foi possível salvar o agendamento:\n{erro}")

    # 5. Botão de confirmação do agendamento
    btn_confirmar = ui.botao(interno, "Confirmar Agendamento", confirmar, variante="sucesso", icone_nome="disponivel")
    btn_confirmar.pack(fill="x", pady=(4, 0))






