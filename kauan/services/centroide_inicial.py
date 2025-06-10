import random

def centroide_inicial(alunos, n=2):
    centroides_iniciais = random.sample(alunos, n)
    c1 = (centroides_iniciais[0].idade, centroides_iniciais[0].nota, centroides_iniciais[0].faltas)
    c2 = (centroides_iniciais[1].idade, centroides_iniciais[1].nota, centroides_iniciais[1].faltas)
    return c1, c2