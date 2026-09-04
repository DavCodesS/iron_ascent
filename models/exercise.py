"""Representacao de um exercicio."""

from dataclasses import dataclass, field


@dataclass
class Exercise:
    nome: str
    categoria: str          # chave de BODY_PARTS, ex: "peito"
    series: int = 3
    repeticoes: int = 10
    peso: float = 0.0
    concluido: bool = False

    def to_dict(self) -> dict:
        """Converte o objeto em dicionario para salvar no JSON."""
        return {
            "nome": self.nome,
            "categoria": self.categoria,
            "series": self.series,
            "repeticoes": self.repeticoes,
            "peso": self.peso,
            "concluido": self.concluido,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Exercise":
        """Cria um Exercise a partir de um dicionario lido do JSON."""
        return cls(
            nome=dados.get("nome", "Exercicio"),
            categoria=dados.get("categoria", "peito"),
            series=int(dados.get("series", 3)),
            repeticoes=int(dados.get("repeticoes", 10)),
            peso=float(dados.get("peso", 0)),
            concluido=bool(dados.get("concluido", False)),
        )
