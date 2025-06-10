
from models.student import Student
from typing import Tuple, List

class Cluster:     
        
    def __init__(self, centroid: Tuple[float, float, float]):
        self.centroid = centroid
        self.students: List[Student] = []
    
    def addStudent(self, student: Student):
        self.students.append(student)
        self.calculate_centroid()
    
    def calculate_centroid(self):
        self.centroid = self.define_centroid()
        
    def define_centroid(self):
        
        age: float = 0.0
        grade: float = 0.0
        absences: float = 0.0
        quantity: float = len(self.students)
        
        if quantity == 0:
            return self.centroid
        
        for student in self.students:
            age += student.age
            grade += student.grade_avg
            absences += student.absences
        
        return (age/quantity, grade/quantity, absences/quantity)
    
    
    def __str__(self):
        return f"{self.centroid} {self.students}"