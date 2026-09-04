"""Responsavel por ler e gravar o arquivo data/data.json.

Nenhuma outra parte do app deve abrir o arquivo diretamente.
Tudo passa por aqui.
"""

import json
import os
from pathlib import Path

from config.ranks import BODY_PARTS
from models.workout import Workout

# Onde gravar o data.json.
# No computador: na pasta data/ do proprio projeto.
# No Android: na pasta privada do app, unico lugar onde ha permissao de escrita.
PASTA_RAIZ = Path(__file__).resolve().parent.parent

if "ANDROID_ARGUMENT" in os.environ:
    PASTA_DADOS = Path(os.environ["ANDROID_PRIVATE"]) / "data"
else:
    PASTA_DADOS = PASTA_RAIZ / "data"

CAMINHO_DADOS = PASTA_DADOS / "data.json"


def estrutura_padrao() -> dict:
    """Formato inicial do arquivo, usado na primeira execucao."""
    return {
        "body_parts": {
            chave: {"xp": 0, "exercicios_concluidos": 0, "treinos_completos": 0}
            for chave in BODY_PARTS
        },
        "treinos": [],
        "historico": [],
    }


class Storage:
    """Guarda os dados em memoria e sincroniza com o disco.

    Os treinos vivem como objetos Workout na lista self.workouts.
    Eles so viram dicionario na hora de gravar o JSON.
    """

    def __init__(self, caminho: Path = CAMINHO_DADOS):
        self.caminho = Path(caminho)
        self.dados = {}
        self.workouts = []
        self.carregar()

    # --- Leitura ------------------------------------------------------------
    def carregar(self) -> dict:
        if self.caminho.exists():
            try:
                with open(self.caminho, "r", encoding="utf-8") as arquivo:
                    self.dados = json.load(arquivo)
            except (json.JSONDecodeError, OSError):
                # Arquivo corrompido ou ilegivel: recomeca do zero em vez de quebrar.
                self.dados = estrutura_padrao()
        else:
            self.dados = estrutura_padrao()

        self._garantir_estrutura()
        self.workouts = [Workout.from_dict(t) for t in self.dados["treinos"]]
        self.salvar()  # garante que data.json existe desde a primeira execucao
        return self.dados

    def _garantir_estrutura(self) -> None:
        """Preenche chaves que faltam.

        Isso permite adicionar uma nova divisao corporal em ranks.py sem
        quebrar um data.json que ja existia.
        """
        padrao = estrutura_padrao()
        for chave, valor in padrao.items():
            self.dados.setdefault(chave, valor)

        for chave, valor in padrao["body_parts"].items():
            atual = self.dados["body_parts"].setdefault(chave, valor)
            for campo, inicial in valor.items():
                atual.setdefault(campo, inicial)

    # --- Escrita ------------------------------------------------------------
    def salvar(self) -> None:
        self.dados["treinos"] = [w.to_dict() for w in self.workouts]
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with open(self.caminho, "w", encoding="utf-8") as arquivo:
            json.dump(self.dados, arquivo, indent=2, ensure_ascii=False)

    # --- Atalhos de leitura -------------------------------------------------
    def body_part(self, chave: str) -> dict:
        return self.dados["body_parts"][chave]

    @property
    def historico(self) -> list:
        return self.dados["historico"]

    def xp_total(self) -> int:
        return sum(parte["xp"] for parte in self.dados["body_parts"].values())

    # --- Treinos ------------------------------------------------------------
    def criar_treino(self, nome: str) -> Workout:
        treino = Workout(nome=nome)
        self.workouts.append(treino)
        self.salvar()
        return treino

    def editar_treino(self, treino: Workout, novo_nome: str) -> None:
        treino.nome = novo_nome
        self.salvar()

    def excluir_treino(self, treino: Workout) -> None:
        if treino in self.workouts:
            self.workouts.remove(treino)
            self.salvar()

    # --- Exercicios ---------------------------------------------------------
    def adicionar_exercicio(self, treino: Workout, exercicio) -> None:
        treino.exercicios.append(exercicio)
        self.salvar()

    def remover_exercicio(self, treino: Workout, exercicio) -> None:
        if exercicio in treino.exercicios:
            treino.exercicios.remove(exercicio)
            self.salvar()

    # --- Progressao ---------------------------------------------------------
    def adicionar_xp(self, categoria: str, quantidade: int) -> None:
        """Soma XP em uma divisao corporal e grava no disco."""
        parte = self.body_part(categoria)
        parte["xp"] += quantidade
        parte["exercicios_concluidos"] += 1
        self.salvar()

    def finalizar_treino(self, treino, xp_por_categoria: dict, concluidos: int) -> None:
        """Fecha um treino: conta o treino nas divisoes e grava no historico."""
        from datetime import date

        for categoria in xp_por_categoria:
            self.body_part(categoria)["treinos_completos"] += 1

        self.registrar_historico({
            "data": date.today().strftime("%d/%m/%Y"),
            "treino": treino.nome,
            "exercicios_concluidos": concluidos,
            "xp": xp_por_categoria,
        })

    def registrar_historico(self, entrada: dict) -> None:
        self.dados["historico"].insert(0, entrada)  # mais recente primeiro
        self.salvar()


# Instancia unica usada pelo app inteiro.
storage = Storage()
