from services.cluster import Cluster
from typing import Tuple, List
from models.aluno import Aluno

class Calcular:
    
    def __init__(self, clusters: List[Cluster]):
        self.clusters = clusters
    
    @staticmethod
    def definir_cluster(aluno: Aluno, cluster1: Cluster, cluster2: Cluster):
        distancia_para_centroide1 = aluno.calcular_distancia_euclidiana(cluster1.centroide)
        distancia_para_centroide2 = aluno.calcular_distancia_euclidiana(cluster2.centroide)
        
        if distancia_para_centroide1 < distancia_para_centroide2:
            cluster1.adicionar_aluno(aluno)
            print(f"Cluster1 {cluster1.alunos}")
            print(f"Distância {distancia_para_centroide1}")
            return cluster1
        cluster2.adicionar_aluno(aluno)
        print(f"Cluster2 {cluster2.alunos}")
        print(f"Distância2 {distancia_para_centroide2}")
        return cluster2

    def definir_cluster_mais_proximo(self, aluno: Aluno):
        clusters_por_distancia: List[Tuple[Cluster, float]] = list(
            map(lambda cluster: (cluster, aluno.calcular_distancia_euclidiana(cluster.centroide)), self.clusters)
        )
        clusters_por_distancia.sort(key=lambda x: x[1])
        
        if len(clusters_por_distancia) == 0:
            return None
        
        return clusters_por_distancia[0][0]

    def calcular_novos_clusters(self):
        for cluster in self.clusters:

            if len(cluster.alunos) == 0:
                continue

            alunos_por_distancia = list(
                map(lambda aluno: (aluno, aluno.calcular_distancia_euclidiana(cluster.centroide)), cluster.alunos)
            )
            alunos_por_distancia.sort(key=lambda x: x[1], reverse=True)

            alunos_mais_distantes = alunos_por_distancia[:len(cluster.alunos) // 3]

            if len(alunos_mais_distantes) == 0:
                continue            
        pass