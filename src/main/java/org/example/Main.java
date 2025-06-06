package org.example;

import java.util.ArrayList;
import java.util.List;


public class Main {
    public static void main(String[] args) {

        //TODO: a distancia entre um elemento longe do centroid e outro elemento longe do centroid
        // deve ser menor do que as suas distancias de seus centros
        List<Student> Allstudents = ReadCSV.readCSV("C:/Users/vinic/IdeaProjects/clusterizacao/src/main/java/org/example/fileStudents.csv");
        List<Student> studentsCluster1 = new ArrayList<>();
        List<Student> studentsCluster2 = new ArrayList<>();

        studentsCluster1.add(Allstudents.getFirst());
        studentsCluster2.add(Allstudents.getLast());

        Cluster cluster1 = new Cluster(Allstudents.getFirst(), studentsCluster1);
        Cluster cluster2 = new Cluster(Allstudents.getLast(), studentsCluster2);

        List<Cluster> clusters = new ArrayList<>();
        clusters.add(cluster1);
        clusters.add(cluster2);

        System.out.println("cluster 1 : " + cluster1);
        System.out.println("-----------------");
        System.out.println("cluster 2 : " + cluster2);
        System.out.println();

        Student student = new Student(20, 7.0, 0.2);
        student.distanceEuclidienne(clusters);
        System.out.println("cluster 1 : " + cluster1);
        System.out.println("-----------------");
        System.out.println("cluster 2 : " + cluster2);
    }
}