"""Calculo de experiencia.

Mantido simples de proposito. Para mudar o balanceamento do jogo,
mexa apenas nas constantes ou na formula abaixo.
"""

XP_BASE = 10
XP_POR_SERIE = 2


def calcular_xp_exercicio(exercicio) -> int:
    """XP ganho ao concluir um exercicio.

    Formula atual: XP = 10 + (series * 2)

    No futuro da para somar bonus por peso ou repeticoes aqui,
    sem precisar alterar nenhuma tela.
    """
    return XP_BASE + (exercicio.series * XP_POR_SERIE)


def calcular_xp_treino(workout) -> dict:
    """Total de XP por categoria se TODOS os exercicios forem concluidos.

    Retorna algo como {"peito": 60, "triceps": 40}.
    Util para mostrar a recompensa antes do treino comecar.
    """
    total = {}
    for exercicio in workout.exercicios:
        xp = calcular_xp_exercicio(exercicio)
        total[exercicio.categoria] = total.get(exercicio.categoria, 0) + xp
    return total
