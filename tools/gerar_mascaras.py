"""Gera as mascaras de cada divisao corporal a partir da imagem original.

Cada divisao e um poligono desenhado por cima da figura. A silhueta recorta
as bordas externas, entao o contorno do corpo fica sempre perfeito.
"""
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
from collections import deque
import numpy as np, json, os


def recortar_fundo(a):
    """Separa a figura do xadrez de transparencia achatado no PNG."""
    h, w, _ = a.shape
    quase_branco = a.min(axis=2) >= 232
    visto = np.zeros((h, w), bool)
    fila = deque()
    for x in range(w):
        for y in (0, h - 1):
            if quase_branco[y, x] and not visto[y, x]:
                visto[y, x] = True
                fila.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if quase_branco[y, x] and not visto[y, x]:
                visto[y, x] = True
                fila.append((y, x))
    while fila:
        y, x = fila.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not visto[ny, nx] and quase_branco[ny, nx]:
                visto[ny, nx] = True
                fila.append((ny, nx))
    # as linhas brancas internas encostam na borda e vazam: seladas aqui
    corpo = ndimage.binary_closing(~visto, structure=np.ones((5, 5)))
    return ndimage.binary_fill_holes(corpo)

ORIGEM = 'tools/corpo_original.png'   # imagem de origem
SAIDA = 'assets/body'
LARGURA = 300
CAIXAS = {"frente": (52, 41, 424, 820), "costas": (477, 41, 849, 820)}

OMBROS = [
    [(28,14),(40,14),(40,22),(36,26),(27,27),(21,24),(22,18)],
    [(72,14),(60,14),(60,22),(64,26),(73,27),(79,24),(78,18)],
]
BRACOS = [
    [(19,26),(30,27),(29,32),(25,38),(15,37),(14,30)],
    [(81,26),(70,27),(71,32),(75,38),(85,37),(86,30)],
]
PERNAS = [[(31,53),(69,53),(70,75),(66,99),(34,99),(30,75)]]

REGIOES = {
    "frente": {
        "ombros":  OMBROS,
        "peito":   [[(38,15),(50,16),(62,15),(63,23),(60,29),(50,31),(40,29),(37,23)]],
        "abdomen": [[(35,29),(65,29),(64,40),(61,48),(50,52),(39,48),(36,40)]],
        "biceps":  BRACOS,
        "pernas":  PERNAS,
    },
    "costas": {
        "ombros":  OMBROS,
        "costas":  [[(36,15),(64,15),(66,24),(62,34),(56,45),(50,48),(44,45),(38,34),(34,24)]],
        "triceps": BRACOS,
        "pernas":  PERNAS,
    },
}

corpo = recortar_fundo(np.array(Image.open(ORIGEM).convert('RGB')))
src = np.array(Image.open(ORIGEM).convert('RGB'))
os.makedirs(SAIDA, exist_ok=True)
mapa = {}

for vista, (x0, y0, x1, y1) in CAIXAS.items():
    silhueta = corpo[y0:y1, x0:x1]
    pixels = src[y0:y1, x0:x1]
    h, w = silhueta.shape
    altura = int(LARGURA * h / w)

    linha = (pixels.min(axis=2) >= 235) & silhueta
    suave = np.array(Image.fromarray((linha * 255).astype('uint8'))
                     .filter(ImageFilter.GaussianBlur(0.7))) / 255.0
    rgb = np.repeat(((0.60 + 0.40 * suave) * 255).astype('uint8')[:, :, None], 3, 2)
    alfa_corpo = (silhueta * 255).astype('uint8')

    def salvar(nome, alfa_arr):
        img = Image.fromarray(np.dstack([rgb, alfa_arr.astype('uint8')]), 'RGBA')
        img.resize((LARGURA, altura), Image.LANCZOS).save(f'{SAIDA}/{vista}_{nome}.png')

    salvar('base', alfa_corpo)

    for nome, poligonos in REGIOES[vista].items():
        mascara = Image.new('L', (w, h), 0)
        desenho = ImageDraw.Draw(mascara)
        for poly in poligonos:
            desenho.polygon([(px / 100 * w, py / 100 * h) for px, py in poly], fill=255)
        salvar(nome, np.minimum(np.array(mascara), alfa_corpo))

    mapa[vista] = {"proporcao": round(LARGURA / altura, 4),
                   "regioes": REGIOES[vista]}

with open(f'{SAIDA}/mapa.json', 'w') as f:
    json.dump(mapa, f, indent=2)
print('ok:', len(os.listdir(SAIDA)), 'arquivos')
