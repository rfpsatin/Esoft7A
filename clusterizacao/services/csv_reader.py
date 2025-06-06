import csv
from typing import List
from models.student import Student


class CSVReader:
    def readCsv(csvfile: str) -> List[Student]:
        students = []
        with open(csvfile, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                student = Student(
                    name=row['nome'],
                    age=int(row['anos']),
                    grade_avg=float(row['media']),
                    absences=float(row['faltas'])                
                )
                students.append(student)
        return students