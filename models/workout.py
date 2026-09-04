"""Representacao de um treino (uma lista de exercicios com nome)."""

from dataclasses import dataclass, field

from models.exercise import Exercise


@dataclass
class Workout:
    nome: str
    exercicios: list = field(default_factory=list)  # lista de Exercise

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "exercicios": [e.to_dict() for e in self.exercicios],
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Workout":
        return cls(
            nome=dados.get("nome", "Treino"),
            exercicios=[Exercise.from_dict(e) for e in dados.get("exercicios", [])],
        )

    def categorias(self) -> list:
        """Divisoes corporais trabalhadas neste treino, sem repetir."""
        vistas = []
        for exercicio in self.exercicios:
            if exercicio.categoria not in vistas:
                vistas.append(exercicio.categoria)
        return vistas
