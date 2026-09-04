"""Converte XP em rank, progresso e proximo objetivo.

Funciona tanto para os ranks de divisao corporal quanto para o rank geral:
basta passar outra tabela no parametro `tabela`.
"""

from config.ranks import RANKS, RANKS_GERAIS


def indice_do_rank(xp: int, tabela: list = RANKS) -> int:
    """Posicao do rank atual dentro da tabela (0 = primeiro rank)."""
    indice = 0
    for posicao, rank in enumerate(tabela):
        if xp >= rank["xp_necessario"]:
            indice = posicao
        else:
            break
    return indice


def rank_atual(xp: int, tabela: list = RANKS) -> dict:
    return tabela[indice_do_rank(xp, tabela)]


def proximo_rank(xp: int, tabela: list = RANKS):
    """Proximo rank, ou None se ja estiver no maximo."""
    indice = indice_do_rank(xp, tabela)
    if indice + 1 < len(tabela):
        return tabela[indice + 1]
    return None


def progresso(xp: int, tabela: list = RANKS) -> dict:
    """Tudo que uma barra de progresso precisa saber.

    Retorna:
        rank            -> dict do rank atual
        proximo         -> dict do proximo rank (ou None)
        xp_no_rank      -> quanto ja andou dentro do rank atual
        xp_necessario   -> quanto o rank atual exige no total para completar
        percentual      -> 0.0 a 1.0
    """
    atual = rank_atual(xp, tabela)
    seguinte = proximo_rank(xp, tabela)

    if seguinte is None:
        return {
            "rank": atual,
            "proximo": None,
            "xp_no_rank": 0,
            "xp_necessario": 0,
            "percentual": 1.0,
        }

    inicio = atual["xp_necessario"]
    fim = seguinte["xp_necessario"]
    faixa = fim - inicio

    return {
        "rank": atual,
        "proximo": seguinte,
        "xp_no_rank": xp - inicio,
        "xp_necessario": faixa,
        "percentual": (xp - inicio) / faixa,
    }


def calcular_rank_geral(body_parts: dict) -> dict:
    """Rank geral do usuario, baseado na soma do XP de todas as divisoes."""
    xp_total = sum(parte["xp"] for parte in body_parts.values())
    resultado = progresso(xp_total, RANKS_GERAIS)
    resultado["xp_total"] = xp_total
    return resultado


def houve_rank_up(xp_antes: int, xp_depois: int, tabela: list = RANKS):
    """Se subiu de rank, devolve o novo rank. Caso contrario, None."""
    if indice_do_rank(xp_depois, tabela) > indice_do_rank(xp_antes, tabela):
        return rank_atual(xp_depois, tabela)
    return None
