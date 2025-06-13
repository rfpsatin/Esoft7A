package org.example;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

public class StudentTest {

    @Test
    public void StudentConstructorTest() {
        Student student = new Student(20, 8.9, 0.9, "");

        assertNotNull(student);
    }

    @Test
    public void getCLusterByNewStudent() {

        Student student1 = new Student(20, 6, 0.9, "");
        Student student2 = new Student(21, 7, 0.9, "");
        Student student3 = new Student(45, 8.6, 0.9, "");
        Student student4 = new Student(51, 9, 0.9, "");

        List<Student> studentsCluster1 = List.of(student1, student2);
        List<Student> studentsCluster2 = List.of(student3, student4);

        Cluster cluster1 = new Cluster(student1, studentsCluster1);
        Cluster cluster2 = new Cluster(student3, studentsCluster2);

        List<Cluster> clusters = List.of(cluster1, cluster2);

        Student newStudent = new Student(23, 6.5, 0.9, "");
        final Cluster cluster = newStudent.calculateMinDistanceEuclidienne(clusters);

        assertEquals(cluster, cluster1);
    }

    @Test
    public void accumulateTest() {

        Student student1 = new Student(20, 6, 0.9, "");
        Student student2 = new Student(21, 7, 0.9, "");

        final Student studentTotal = student1.accumule(student2);

        assertEquals(41, studentTotal.getAge());
        assertEquals(13, studentTotal.getAverage());
        assertEquals(1.8, studentTotal.getAbscense());
    }

    @Test
    public void throwExceptionWhenDivisorMenor1() {

        Student student1 = new Student(20, 6, 0.9, "");

        Assertions.assertThrows(IllegalArgumentException.class,
                () -> student1.divide(0),
                "Divisor deve ser maior que 0");
    }

    @Test
    public void divisor() {

        Student student1 = new Student(20, 6, 0.9, "");

        student1.divide(3);

        assertEquals(6, student1.getAge());
        assertEquals(2.0, student1.getAverage());
        assertEquals(0.3, student1.getAbscense());
    }

}
