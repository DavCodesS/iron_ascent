"""Dados de configuracao do sistema de progressao.

Este arquivo contem SOMENTE dados. Nenhuma logica.
Para mudar os nomes dos ranks ou a dificuldade da progressao,
altere apenas as listas abaixo.
"""

# --- Divisoes corporais -----------------------------------------------------
# A chave (ex: "peito") e o identificador usado no data.json.
# O label e o texto mostrado na tela.
# "curto" e usado no painel compacto da tela inicial.
BODY_PARTS = {
    "peito":   {"label": "PEITO",   "curto": "PEI", "icon": "arm-flex"},
    "costas":  {"label": "COSTAS",  "curto": "COS", "icon": "human-handsup"},
    "pernas":  {"label": "PERNAS",  "curto": "PER", "icon": "run"},
    "ombros":  {"label": "OMBROS",  "curto": "OMB", "icon": "weight-lifter"},
    "biceps":  {"label": "BICEPS",  "curto": "BIC", "icon": "dumbbell"},
    "triceps": {"label": "TRICEPS", "curto": "TRI", "icon": "karate"},
    "abdomen": {"label": "ABDOMEN", "curto": "ABD", "icon": "shield-outline"},
}

# --- Ranks de cada divisao corporal -----------------------------------------
# A lista PRECISA estar em ordem crescente de xp_necessario.
# A cor sobe junto com o rank: cinza cru -> metais -> fogo -> plasma -> ouro.
RANKS = [
    {"nome": "RECRUTA",            "xp_necessario": 0,    "cor": "#6E7681"},
    {"nome": "SOLDADO",            "xp_necessario": 100,  "cor": "#8B9A5B"},
    {"nome": "GUERREIRO DE FERRO", "xp_necessario": 250,  "cor": "#A97142"},
    {"nome": "VETERANO",           "xp_necessario": 500,  "cor": "#B9C2CC"},
    {"nome": "COMANDANTE",         "xp_necessario": 900,  "cor": "#F0A31E"},
    {"nome": "TANQUE DE FERRO",    "xp_necessario": 1500, "cor": "#E2703A"},
    {"nome": "TANQUE DE GUERRA",   "xp_necessario": 2400, "cor": "#D9483B"},
    {"nome": "COLOSSO DE ACO",     "xp_necessario": 3600, "cor": "#9B5DE5"},
    {"nome": "MAQUINA DE GUERRA",  "xp_necessario": 5200, "cor": "#22D3EE"},
    {"nome": "LENDA DO ACO",       "xp_necessario": 7500, "cor": "#FFD447"},
]

# --- Rank geral -------------------------------------------------------------
# Calculado a partir da soma do XP de todas as divisoes corporais.
# Por isso os valores sao bem maiores.
RANKS_GERAIS = [
    {"nome": "CIVIL",               "xp_necessario": 0,     "cor": "#6E7681"},
    {"nome": "ALISTADO",            "xp_necessario": 300,   "cor": "#8B9A5B"},
    {"nome": "SOLDADO DE ACO",      "xp_necessario": 1000,  "cor": "#A97142"},
    {"nome": "OPERADOR",            "xp_necessario": 2500,  "cor": "#B9C2CC"},
    {"nome": "VETERANO DE ACO",     "xp_necessario": 5000,  "cor": "#F0A31E"},
    {"nome": "COMANDANTE DE FERRO", "xp_necessario": 9000,  "cor": "#E2703A"},
    {"nome": "COLOSSO",             "xp_necessario": 16000, "cor": "#D9483B"},
    {"nome": "MAQUINA DE GUERRA",   "xp_necessario": 28000, "cor": "#22D3EE"},
    {"nome": "LENDA DO ACO",        "xp_necessario": 45000, "cor": "#FFD447"},
]
