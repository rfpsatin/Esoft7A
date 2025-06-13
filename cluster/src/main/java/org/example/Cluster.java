package org.example;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Cluster {

    private Student centroid;

    private final List<Student> students = new ArrayList<>();

    public Cluster(Student centroid, List<Student> students) {
        this.centroid = centroid;
        this.students.addAll(students);
    }

    public Student recalcutecentroid(List<Student> students) {

        int size = students.size();
        final Student student = students
                .stream()
                .reduce(Student.of(), Student::accumule);

        student.divide(size);
        return this.centroid = student;
    }

    public void addStudent(Student newStudent) {
        this.students.add(newStudent);
        recalcutecentroid(students);
    }

    public double calculatedDistance(Student student, Student centroid) {
        double sum = 0;
        sum += Math.pow(student.getAge() - centroid.getAge(), 2);
        sum += Math.pow(student.getAverage() - centroid.getAverage(), 2);
        sum += Math.pow(student.getAbscense() - centroid.getAbscense(), 2);

        for (int i = 0; i < student.getEncodedCategory().size(); i++) {
            double val1 = student.getEncodedCategory().get(i);
            double val2 = centroid.getEncodedCategory().get(i);
            sum += Math.pow(val1 - val2, 2);
        }

        return Math.sqrt(sum);
    }

    public static Cluster tryCreateNewCluster(Cluster clusterA, Cluster clusterB) {

        Student outlierA = clusterA.getStudents().stream()
                .max(Comparator.comparingDouble(student -> clusterA.calculatedDistance(student, clusterA.getCentroid())))
                .orElse(null);

        System.out.println("elemento mais distante do cluster A: " + outlierA);

        Student outlierB = clusterB.getStudents().stream()
                .max(Comparator.comparingDouble(student -> clusterB.calculatedDistance(student, clusterB.getCentroid())))
                .orElse(null);

        System.out.println("elemento mais distante do cluster B: " + outlierB);

        double distanceAB = clusterB.calculatedDistance(outlierA, outlierB);

        System.out.println("distancia do A ao B: " + distanceAB);

        double distanceAtoCentroid = clusterA.calculatedDistance(outlierA, clusterA.getCentroid());
        System.out.println("distancia do A ao centroide: " + distanceAtoCentroid);
        double distanceBtoCentroid = clusterB.calculatedDistance(outlierB, clusterB.getCentroid());
        System.out.println("distancia do B ao centroide: " + distanceAtoCentroid);

        if (distanceAB < distanceAtoCentroid && distanceAB < distanceBtoCentroid) {
            List<Student> newListStudents = List.of(outlierA, outlierB);
            clusterA.getStudents().remove(outlierA);
            clusterA.recalcutecentroid(clusterA.getStudents());

            clusterB.getStudents().remove(outlierB);
            clusterB.recalcutecentroid(clusterB.getStudents());
            return new Cluster(outlierA, newListStudents);
        }
        return null;
    }

    public List<Student> getStudents() {
        return students;
    }

    public Student getCentroid() {
        return centroid;
    }


    @Override
    public String toString() {
        return "Cluster{" +
                "centroid=" + centroid +
                ", students=" + students +
                '}';
    }
}
