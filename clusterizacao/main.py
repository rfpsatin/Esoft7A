from services.csv_reader import CSVReader
from services.initial_centroid import initial_centroid
from services.cluster import Cluster
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
            
    for cluster in calculate.clusters:
        print(f"Cluster: {cluster}")
        
    pass

    

    
    
if __name__ == "__main__":
    main()