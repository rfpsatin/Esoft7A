class Registro:
    def _init_(self, x, y, is_centroide=False):
        self.x = x
        self.y = y
        self.is_centroide = is_centroide
        self.cluster = None

class Cluster:
    def _init_(self, centroide):
        self.centroide = centroide
        self.registros = [centroide]

    def atualizar_centroide(self):
        soma_x = 0
        soma_y = 0
        n = 0
        for r in self.registros:
            soma_x += r.x
            soma_y += r.y
            n += 1
        self.centroide = Registro(soma_x / n, soma_y / n, True)

def distancia(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    return (dx * dx + dy * dy) ** 0.5

def limpar_clusters(clusters):
    for c in clusters:
        c.registros = [c.centroide]

def atribuir_clusters(registros, clusters):
    for r in registros:
        menor = None
        menor_dist = None
        for c in clusters:
            d = distancia(r, c.centroide)
            if menor_dist is None or d < menor_dist:
                menor_dist = d
                menor = c
        menor.registros.append(r)
        r.cluster = menor

def executar_kmeans(registros, centroides, iteracoes):
    clusters = [Cluster(c) for c in centroides]
    for _ in range(iteracoes):
        limpar_clusters(clusters)
        atribuir_clusters(registros, clusters)
        for c in clusters:
            c.atualizar_centroide()
    return clusters

registros = [Registro(1, 2), Registro(2, 1), Registro(3, 3), Registro(8, 8), Registro(9, 10), Registro(10, 9)]
centroides = [Registro(1, 2, True), Registro(8, 8, True)]
clusters = executar_kmeans(registros, centroides, 5)

for c in clusters:
    print(f'{c.centroide.x:.2f} {c.centroide.y:.2f}')
    for r in c.registros:
        print(f'{r.x} {r.y}')