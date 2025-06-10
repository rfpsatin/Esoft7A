from services.leitorcsv import LeitorCSV
from services.centroide_inicial import centroide_inicial
from services.cluster import Cluster
from services.calcular import Calcular

def main():
    csv_file = 'alunos1.csv'
    students = LeitorCSV.ler_csv(csv_file)
    initialCentroids = centroide_inicial(students)
    initialClusters = [Cluster(initialCentroids[0]), Cluster(initialCentroids[1])]
    calculate = Calcular(initialClusters)
    
    for student in students:
        cluster = calculate.definir_cluster(student, initialClusters[0], initialClusters[1])
    
    for cluster in calculate.clusters:
        print(f"Cluster: {cluster}")
        
    pass

    

    
    
if __name__ == "__main__":
    main()