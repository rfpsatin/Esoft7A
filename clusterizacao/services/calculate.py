import numpy as np
from models.cluster import Cluster
from typing import Tuple
from models.student import Student
from typing import List


class Calculate:
    
    def __init__(self, clusters: List[Cluster]):
        self.clusters = clusters
    
  
    def define_cluster_2(self, student: Student):
        
        clustersByDistance: List[Tuple[Cluster, float]] = list(map(lambda cluster: (cluster, student.calculate_euclidean_distance(cluster.centroid)), self.clusters))
        clustersByDistance.sort(key=lambda x: x[1])
        
        if (len(clustersByDistance) == 0):
            return None
        
        return clustersByDistance[0][0]
    
    
    def calculate_new_cluster(self, min_students: int = 6) -> bool:
        candidate_students = []

        for i, current_cluster in enumerate(self.clusters):
            students_in_cluster = current_cluster.students
            current_centroid = current_cluster.centroid

            if not students_in_cluster:
                continue

            distances_to_centroid = [
                student.calculate_euclidean_distance(current_centroid)
                for student in students_in_cluster
            ]
            print(f"Distâncias para o centroide: {distances_to_centroid}")

            if len(distances_to_centroid) > 1:
                mean_distance = np.mean(distances_to_centroid)
                print(f"Distância média {mean_distance}")
            else:
                mean_distance = distances_to_centroid[0] if distances_to_centroid else 0

            limiar = mean_distance
            print(f"Novo limiar: {limiar}")

            distant_students_index = [
                index for index, distance in enumerate(distances_to_centroid)
                if distance > limiar
            ]

            for index in distant_students_index:
                student = students_in_cluster[index]
                min_distance_to_other = float('inf')

                for j, other_cluster in enumerate(self.clusters):
                    if i == j:
                        continue
                    other_centroid = other_cluster.centroid
                    distance = student.calculate_euclidean_distance(other_centroid)

                    if distance < min_distance_to_other:
                        min_distance_to_other = distance

                if min_distance_to_other != float('inf'):
                    candidate_students.append((min_distance_to_other, student, i))

        if not candidate_students:
            print("Nenhum estudante encontrado para formar um novo cluster")
            return False

        if len(candidate_students) < min_students:
            print(f"Não há {min_students} estudantes suficientes para formar um novo cluster")
            return False

        candidate_students.sort(key=lambda x: x[0])

        top_candidate_students = candidate_students[:min_students]
        students_to_move = [c[1] for c in top_candidate_students]

    
        original_students = self.clusters[top_candidate_students[0][2]].students
        remaining_students = [student for student in original_students if student not in students_to_move]

        self.clusters[top_candidate_students[0][2]].students = remaining_students

        if students_to_move:
            ages = [s.age for s in students_to_move]
            grades = [s.grade_avg for s in students_to_move]
            absences = [s.absences for s in students_to_move]
            new_centroid = (int(np.mean(ages)), np.mean(grades), np.mean(absences))

            new_cluster = Cluster(centroid=new_centroid)
            new_cluster.students = students_to_move

            new_cluster.calculate_centroid()

            self.clusters.append(new_cluster)
            self.clusters[top_candidate_students[0][2]].calculate_centroid()

            return True

        return False

            
        
        # for cluster in self.clusters:
            
        #     if len(studentsByDistance) == 0:
        #         continue
            
        #     studentsByDistance = list(map(lambda student: (student, student.calculate_euclidean_distance(cluster.centroid)), cluster.students))
        #     studentsByDistance.sort(key=lambda x: x[1], reverse=True)
            
        #     studentsMaisDistantes = studentsByDistance[:len(cluster.students) / 3]
                        
        #     if len(studentsMaisDistantes) == 0:
        #         continue
        # pass