"""Identidade visual do IRON ASCENT.

Todas as cores ficam aqui. Se voce quiser mudar o visual do app inteiro,
basta alterar este arquivo.
"""

from kivy.utils import get_color_from_hex as hex_color

# --- Cores base -------------------------------------------------------------
BG = hex_color("#0B0D10")            # fundo da tela
SURFACE = hex_color("#151A21")       # fundo dos cards
SURFACE_LIGHT = hex_color("#1E252E")  # cards em destaque
BORDER = hex_color("#2C343F")        # linhas e contornos
BONECO_NEUTRO = hex_color("#333D4A")  # partes do boneco sem rank

# --- Cores de acento --------------------------------------------------------
ACCENT = hex_color("#F0A31E")        # ambar industrial (cor principal)
ACCENT_DARK = hex_color("#7A5410")   # ambar apagado (fundo de barras)
STEEL = hex_color("#5B6B7F")         # azul aco
SUCCESS = hex_color("#4CAF7D")
DANGER = hex_color("#D9483B")

# --- Texto ------------------------------------------------------------------
TEXT = hex_color("#E6EAF0")
TEXT_DIM = hex_color("#8A94A3")
TEXT_MUTED = hex_color("#5A6472")

# --- Espacamentos -----------------------------------------------------------
PADDING = 16
GAP = 12
RADIUS = 10


def cor(valor_hex: str):
    """Converte "#F0A31E" no formato de cor que o Kivy entende."""
    return hex_color(valor_hex)
