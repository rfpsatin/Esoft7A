from services.cluster import Cluster
from typing import Tuple
from models.student import Student
from typing import List

class Calculate:
    
    def __init__(self, clusters: List[Cluster]):
        self.clusters = clusters
    
    def define_cluster(student: Student, cluster1: Cluster, cluster2: Cluster):
        distance_from_centroid1 = student.calculate_euclidean_distante(cluster1.centroid)
        distance_from_centroid2 = student.calculate_euclidean_distante(cluster2.centroid)
        
        if distance_from_centroid1 < distance_from_centroid2:
            cluster1.addStudent(student)
            print(f"Cluster1 {cluster1.students}")
            print(f"Distância {distance_from_centroid1}")
            return cluster1
        cluster2.addStudent(student)
        print(f"Cluster2 {cluster1.students}")
        print(f"Distância2 {distance_from_centroid2}")
        return cluster2

    
    def define_cluster_2(self, student: Student):
        
        clustersByDistance: List[Tuple[Cluster, float]] = list(map(lambda cluster: (cluster, student.calculate_euclidean_distante(cluster.centroid)), self.clusters))
        clustersByDistance.sort(key=lambda x: x[1])
        
        if (len(clustersByDistance) == 0):
            return None
        
        return clustersByDistance[0][0]
    
    
    def calculate_new_cluster(self):
        
        for cluster in self.clusters:
            
            if len(studentsByDistance) == 0:
                continue
            
            studentsByDistance = list(map(lambda student: (student, student.calculate_euclidean_distante(cluster.centroid)), cluster.students))
            studentsByDistance.sort(key=lambda x: x[1], reverse=True)
            
            studentsMaisDistantes = studentsByDistance[:len(cluster.students) / 3]
                        
            if len(studentsMaisDistantes) == 0:
                continue
            
            
            
            
        
        pass