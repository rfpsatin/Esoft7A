
import math
import matplotlib.pyplot as plt

class Registro:
    def __init__(self, id, atributos, e_centroid=False, categoria=None):
        self.id = id
        self.atributos = atributos
        self.e_centroid = e_centroid
        self.categoria = categoria

class Cluster:
    def __init__(self, id):
        self.id = id
        self.registros = []
        self.centroid = None

    def inserir_registro(self, registro):
        self.registros.append(registro)
        self.recalcular_centroid()

    def remover_registro(self, registro_id):
        self.registros = [r for r in self.registros if r.id != registro_id]
        self.recalcular_centroid()

    def alterar_registro(self, registro_id, novos_atributos):
        for r in self.registros:
            if r.id == registro_id:
                r.atributos = novos_atributos
        self.recalcular_centroid()

    def recalcular_centroid(self):
        if not self.registros:
            self.centroid = None
            return
        media = [sum(attr[i] for attr in [r.atributos for r in self.registros]) / len(self.registros)
                 for i in range(len(self.registros[0].atributos))]
        self.centroid = media

def distancia_euclidiana(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def atribuir_registro_clusters(registro, clusters):
    distancias = [(cluster, distancia_euclidiana(registro.atributos, cluster.centroid)) for cluster in clusters]
    cluster_mais_proximo = min(distancias, key=lambda x: x[1])[0]
    cluster_mais_proximo.inserir_registro(registro)

def atualizar_centroid_real(cluster):
    cluster.recalcular_centroid()
    if cluster.registros:
        mais_proximo = min(cluster.registros, key=lambda r: distancia_euclidiana(r.atributos, cluster.centroid))
        for r in cluster.registros:
            r.e_centroid = (r == mais_proximo)

def criar_novo_cluster_se_necessario(clusters, limiar):
    novos_clusters = []
    for cluster in clusters:
        for r in cluster.registros[:]:
            distancia = distancia_euclidiana(r.atributos, cluster.centroid)
            if distancia > limiar:
                outros = [c for c in clusters if c != cluster]
                if outros and distancia_euclidiana(r.atributos, outros[0].centroid) < distancia:
                    cluster.remover_registro(r.id)
                    novo = Cluster(id=len(clusters) + len(novos_clusters) + 1)
                    novo.inserir_registro(r)
                    novos_clusters.append(novo)
    clusters.extend(novos_clusters)

def codificar_categorias(registros):
    categorias_unicas = list(set(r.categoria for r in registros if r.categoria))
    mapeamento = {cat: i for i, cat in enumerate(categorias_unicas)}
    for r in registros:
        if r.categoria:
            r.atributos.append(mapeamento[r.categoria])

registros = [
    Registro(1, [1.0, 2.0], True),
    Registro(2, [9.0, 10.0], True),
    Registro(3, [2.0, 1.5], categoria='A'),
    Registro(4, [8.0, 9.0], categoria='B'),
    Registro(5, [1.5, 2.2], categoria='A'),
    Registro(6, [7.5, 8.5], categoria='B'),
]

codificar_categorias(registros)

cluster1 = Cluster(1)
cluster2 = Cluster(2)
cluster1.inserir_registro(registros[0])
cluster2.inserir_registro(registros[1])
clusters = [cluster1, cluster2]

for registro in registros[2:]:
    atribuir_registro_clusters(registro, clusters)

for cluster in clusters:
    atualizar_centroid_real(cluster)

criar_novo_cluster_se_necessario(clusters, limiar=3.0)

cores = ['red', 'blue', 'green', 'orange', 'purple']
fig, ax = plt.subplots()

for i, cluster in enumerate(clusters):
    for r in cluster.registros:
        ax.scatter(r.atributos[0], r.atributos[1], color=cores[i], marker='x' if r.e_centroid else 'o')
    if cluster.centroid:
        ax.scatter(cluster.centroid[0], cluster.centroid[1], color=cores[i], marker='D', s=100, label=f'Centróide C{cluster.id}')

ax.legend()
ax.set_title("Visualização dos Clusters com Centróides")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.tight_layout()
plt.show()
