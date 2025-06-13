package org.example;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

public class ClusterTest {

    @Test
    public void testCluster() {
        Student student = new Student(20, 8.9, 0.9, "");
        List<Student> students = new ArrayList<>();
        Cluster cluster = new Cluster(student, students);

        Assertions.assertNotNull(cluster);
    }

    @Test
    public void recalcutecentroidTest() {
        Student newStudent1 = new Student(20, 8.9, 0.9, "");
        Student newStudent2 = new Student(23, 4.5, 0.9, "");

        List<Student> students = new ArrayList<>();
        students.add(newStudent1);

        Cluster cluster = new Cluster(newStudent1, students);

        Student inicialCentroid = cluster.recalcutecentroid(cluster.getStudents());

        cluster.addStudent(newStudent2);

        Student finalCentroid = cluster.recalcutecentroid(cluster.getStudents());

        System.out.println("centroid inicial: " + inicialCentroid);
        System.out.println("centroid final: " + finalCentroid);
        Assertions.assertNotEquals(inicialCentroid, finalCentroid);

    }

    @Test
    public void addStudentTest() {
        Student inicialStudent = new Student(20, 8.9, 0.9, "");
        List<Student> students = new ArrayList<>();
        students.add(inicialStudent);

        Cluster cluster = new Cluster(inicialStudent, students);

        Student student = new Student(56, 7.0, 0.1, "");
        cluster.addStudent(student);

        Assertions.assertEquals(2, cluster.getStudents().size());
    }

    @Test
    public void calculateDistanceEuclidienneTest() {
        Student centroid = new Student(20, 8.9, 0.9, "");
        Student newStudent = new Student(45, 9.0, 0.1, "");

        List<Student> students = new ArrayList<>();
        students.add(centroid);

        Cluster cluster = new Cluster(centroid, students);
        double distance = cluster.calculatedDistance(newStudent, cluster.getCentroid());

        System.out.println(distance);

        Assertions.assertEquals(25, distance, 0.1);
    }


}
