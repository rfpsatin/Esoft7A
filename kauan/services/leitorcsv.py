import csv
from typing import List
from models.aluno import Aluno

class LeitorCSV:
    @staticmethod
    def ler_csv(arquivo_csv: str) -> List[Aluno]:
        alunos = []
        with open(arquivo_csv, mode='r') as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                aluno = Aluno(
                    nome=linha['nome'],
                    idade=int(linha['anos']),
                    nota=float(linha['media']),
                    faltas=float(linha['faltas'])                
                )
                alunos.append(aluno)
        return alunos