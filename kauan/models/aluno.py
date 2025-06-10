from dataclasses import dataclass
from services.distancia_euclidiana import distancia_euclidiana
from typing import Tuple

@dataclass
class Aluno:
    nome: str
    idade: int
    nota: float
    faltas: float

    def calcular_distancia_euclidiana(self, centroide: Tuple[int, float, float]):
        return distancia_euclidiana(centroide, (self.idade, self.nota, self.faltas))

    def __str__(self):
        return f"{self.nome} {self.idade} {self.nota} {self.faltas}"