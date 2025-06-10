from models.aluno import Aluno
from typing import Tuple, List

class Cluster:     
        
    def __init__(self, centroide: Tuple[float, float, float]):
        self.centroide = centroide
        self.alunos: List[Aluno] = []
    
    def adicionar_aluno(self, aluno: Aluno):
        self.alunos.append(aluno)
        self.calcular_centroide()
    
    def calcular_centroide(self):
        self.centroide = self.definir_centroide()
        
    def definir_centroide(self):
        idade_total: float = 0.0
        nota_total: float = 0.0
        faltas_total: float = 0.0
        quantidade: float = len(self.alunos)
        
        if quantidade == 0:
            return self.centroide
        
        for aluno in self.alunos:
            idade_total += aluno.idade
            nota_total += aluno.nota
            faltas_total += aluno.faltas
        
        return (
            idade_total / quantidade,
            nota_total / quantidade,
            faltas_total / quantidade
        )
    
    def __str__(self):
        return f"{self.centroide} {self.alunos}"