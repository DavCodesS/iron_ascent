# IRON ASCENT

App de treino gamificado. Parte 1: nucleo de progressao + tela inicial.

## Como rodar (Windows / VSCode)

    py -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python main.py

Os dados ficam em `data/data.json`, criado automaticamente.

## Telas

- HOME — rank geral, boneco com as cores dos ranks e navegacao
- MEU PROGRESSO — as 7 divisoes corporais
- DETALHE DA DIVISAO — rank, XP e estatisticas
- MEUS TREINOS — criar, renomear e excluir treinos
- TREINO — adicionar e remover exercicios
- TREINO ATIVO — concluir exercicios e ganhar XP
- HISTORICO — treinos finalizados

## Boneco anatomico

As imagens de `assets/body/` sao mascaras em branco: o app multiplica cada
uma pela cor do rank da divisao. Para mudar o traçado dos musculos, edite os
poligonos em `tools/gerar_mascaras.py` e rode, a partir da raiz do projeto:

    pip install pillow numpy scipy
    python tools/gerar_mascaras.py

## Gerar o APK

Precisa de Linux (no Windows, use o WSL). A partir da raiz do projeto:

    pip install buildozer cython
    buildozer -v android debug

O APK sai em `bin/`. A primeira compilacao baixa o Android SDK e NDK e
demora de 30 a 60 minutos.

### Gerar o APK sem instalar nada

Suba o projeto para um repositorio no GitHub. O arquivo
`.github/workflows/build-apk.yml` compila automaticamente e o APK fica
disponivel na aba **Actions**, em Artifacts.
