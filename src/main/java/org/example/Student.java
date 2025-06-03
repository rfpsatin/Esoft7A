package org.example;

import java.util.Comparator;
import java.util.List;

public class Student {

    private Integer age;

    private double average;

    private double abscense;

    public Student(Integer age, double average, double abscense) {
        this.age = age;
        this.average = average;
        this.abscense = abscense;
    }

    public static Student of() {
        return new Student(0, 0, 0);
    }

    public Student accumule(final Student student) {
        age += student.getAge();
        average += student.getAverage();
        abscense += student.getAbscense();

        return this;
    }

    public void divide(final int divisor) {

        if (divisor < 1) {
            throw new IllegalArgumentException("Divisor deve ser maior que 0");
        }

        age = age / divisor;
        average = average / divisor;
        abscense = abscense / divisor;
    }

    public void distanceEuclidienne(List<Cluster> clusters) {

        Cluster cluster = clusters.stream()
                .min(Comparator.comparingDouble(c -> c.calculatedDistance(this, c.getCentroid())))
                .orElseThrow();

        cluster.addStudent(this);
    }

    public Integer getAge() {
        return age;
    }

    public double getAverage() {
        return average;
    }

    public double getAbscense() {
        return abscense;
    }

    @Override
    public String toString() {
        return "Student{" +
                "age=" + age +
                ", average=" + average +
                ", abscense=" + abscense +
                '}';
    }
}
