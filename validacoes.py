# ============================================================
# VALIDACOES.PY - regras de validacao reutilizaveis
# Criado por Dener em 25/06/2026
# ------------------------------------------------------------
# Funcoes que conferem se um dado digitado e valido (CPF, CNPJ,
# e-mail, telefone) e funcoes que formatam (poem os pontos/tracos).
# Ficam aqui, separadas das telas, para poderem ser reaproveitadas
# e testadas com facilidade.
# ============================================================

import re


def so_digitos(texto):
    """Devolve apenas os numeros do texto (tira pontos, tracos, espacos...)."""
    return "".join(ch for ch in texto if ch.isdigit())


def validar_cpf(cpf):
    """True se o CPF for valido (11 digitos + digitos verificadores corretos)."""
    cpf = so_digitos(cpf)
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:          # 000... , 111... etc. sao invalidos
        return False

    # 1o digito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10) % 11
    if d1 == 10:
        d1 = 0
    if d1 != int(cpf[9]):
        return False

    # 2o digito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10) % 11
    if d2 == 10:
        d2 = 0
    return d2 == int(cpf[10])


def validar_cnpj(cnpj):
    """True se o CNPJ for valido (14 digitos + digitos verificadores corretos)."""
    cnpj = so_digitos(cnpj)
    if len(cnpj) != 14:
        return False
    if cnpj == cnpj[0] * 14:
        return False

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    d1 = soma % 11
    d1 = 0 if d1 < 2 else 11 - d1
    if d1 != int(cnpj[12]):
        return False

    soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    d2 = soma % 11
    d2 = 0 if d2 < 2 else 11 - d2
    return d2 == int(cnpj[13])


def validar_email(email):
    """True se o e-mail tiver um formato basico valido (algo@algo.algo)."""
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()) is not None


def validar_telefone(telefone):
    """True se o telefone tiver 10 (fixo) ou 11 (celular) digitos."""
    return len(so_digitos(telefone)) in (10, 11)


def formatar_cpf(cpf):
    """Poe a mascara do CPF: 000.000.000-00."""
    c = so_digitos(cpf)
    if len(c) != 11:
        return cpf
    return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"


def formatar_cnpj(cnpj):
    """Poe a mascara do CNPJ: 00.000.000/0000-00."""
    c = so_digitos(cnpj)
    if len(c) != 14:
        return cnpj
    return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"


def formatar_telefone(telefone):
    """Poe a mascara do telefone: (00) 0000-0000 ou (00) 00000-0000."""
    n = so_digitos(telefone)
    if len(n) == 10:
        return f"({n[:2]}) {n[2:6]}-{n[6:]}"
    if len(n) == 11:
        return f"({n[:2]}) {n[2:7]}-{n[7:]}"
    return telefone
