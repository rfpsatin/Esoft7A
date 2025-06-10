import math
from typing import Tuple

def distancia_euclidiana(centroide: Tuple[int, float, float], aluno: Tuple[int, float, float]) -> float:
    return math.sqrt(
        (centroide[0] - aluno[0])**2 +
        (centroide[1] - aluno[1])**2 +
        (centroide[2] - aluno[2])**2
    )