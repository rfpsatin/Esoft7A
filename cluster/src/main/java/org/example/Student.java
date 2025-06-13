package org.example;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Student {

    private Integer age;

    private double average;

    private double abscense;

    private String category;

    private List<Double> encodedCategory = new ArrayList<>();

    public Student(Integer age, double average, double abscense, String categoryCourse) {
        this.age = age;
        this.average = average;
        this.abscense = abscense;
        this.category = categoryCourse;
    }

    public void encodeCourseCategory(List<String> allCategories) {
        encodedCategory = new ArrayList<>();
        for (String category : allCategories) {
            encodedCategory.add(category.equals(this.category) ? 1.0 : 0.0);
        }
    }

    public static Student of() {

        return new Student(0, 0, 0, "");
    }

    public Student accumule(final Student student) {
        age += student.getAge();
        average += student.getAverage();
        abscense += student.getAbscense();

        if (this.encodedCategory.isEmpty() && !student.getEncodedCategory().isEmpty()) {
            encodedCategory = new ArrayList<>();
            for (int i = 0; i < student.getEncodedCategory().size(); i++) {
                encodedCategory.add(0.0);
            }
        }

        for (int i = 0; i < encodedCategory.size(); i++) {
            encodedCategory.set(i, encodedCategory.get(i) + student.getEncodedCategory().get(i));
        }

        return this;
    }

    public void divide(final int divisor) {

        if (divisor < 1) {
            throw new IllegalArgumentException("Divisor deve ser maior que 012");
        }

        age = age / divisor;
        average = average / divisor;
        abscense = abscense / divisor;

        encodedCategory.replaceAll(aDouble -> aDouble / divisor);
    }

    public Cluster calculateMinDistanceEuclidienne(List<Cluster> clusters) {

        Cluster cluster = clusters.stream()
                .min(Comparator.comparingDouble(c -> c.calculatedDistance(this, c.getCentroid())))
                .orElseThrow();

        cluster.addStudent(this);
        return cluster;
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

    public String getCategory() {
        return category;
    }

    public List<Double> getEncodedCategory() {
        return encodedCategory;
    }

    public void setEncodedCategory(List<Double> encodedCategory) {
        this.encodedCategory = encodedCategory;
    }

    @Override
    public String toString() {
        return "Student{" +
                "age=" + age +
                ", average=" + average +
                ", abscense=" + abscense +
                ", category='" + category + '\'' +
                ", encodedCategory=" + encodedCategory +
                '}';
    }
}
