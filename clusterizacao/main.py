from models.student import Student
from services.csv_reader import CSVReader
from services.initial_centroid import initial_centroid
from models.cluster import Cluster
from services.calculate import Calculate

def main():
    csv_file = 'alunos1.csv'
    students = CSVReader.readCsv(csv_file)
    initialCentroids = initial_centroid(students)
    initialClusters = [Cluster(initialCentroids[0]), Cluster(initialCentroids[1])]
    calculate = Calculate(initialClusters)
    
    for student in students:
        cluster = calculate.define_cluster_2(student)
        
        if (cluster):
            cluster.addStudent(student)
    
    new_cluster = calculate.calculate_new_cluster(min_students=6)
    print(f"Novo cluster: {new_cluster}")
 
    for idx, cluster in enumerate(calculate.clusters):
        print(f"\n Cluster {idx + 1} - Centroide: {cluster.centroid}")
        for student in cluster.students:
            print(f"  - {student}")
    
    
if __name__ == "__main__":
    main()