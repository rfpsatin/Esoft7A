import math
from typing import Tuple

def euclidian_distance(centroid: Tuple[int, float, float], student: Tuple[int, float, float]) -> float:
    return math.sqrt(
        (centroid[0] - student[0])**2 +
        (centroid[1] - student[1])**2 +
        (centroid[2] - student[2])**2
    )