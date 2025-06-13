package org.example;

import java.util.ArrayList;
import java.util.List;


public class Main {
    public static void main(String[] args) {

        List<Student> allstudents = ReadCSV.readCSV("C:/Users/vinic/IdeaProjects/clusterizacao/src/main/java/org/example/fileStudents.csv");
        List<Student> studentsCluster1 = new ArrayList<>();
        List<Student> studentsCluster2 = new ArrayList<>();

        studentsCluster1.add(allstudents.get(0));
        studentsCluster2.add(allstudents.get(1));

        Cluster cluster1 = new Cluster(allstudents.get(0), studentsCluster1);
        Cluster cluster2 = new Cluster(allstudents.get(1), studentsCluster2);

        List<Cluster> clusters = new ArrayList<>();

        clusters.add(cluster1);
        clusters.add(cluster2);

        allstudents.stream()
                .skip(2)
                .forEach(student -> {
                    student.calculateMinDistanceEuclidienne(clusters);
                });

        System.out.println("cluster 1 : " + cluster1);
        System.out.println();
        System.out.println("cluster 2 : " + cluster2);
        System.out.println();

        System.out.println("alunos no cluster 1: " + cluster1.getStudents().size());
        System.out.println("alunos no cluster 2: " + cluster2.getStudents().size());
        System.out.println();

        Cluster cluster3 = Cluster.tryCreateNewCluster(cluster1, cluster2);

        System.out.println("cluster 1 : " + cluster1);
        System.out.println();
        System.out.println("cluster 2 : " + cluster2);
        System.out.println();
        System.out.println("cluster 3: " + cluster3);
        System.out.println();
        System.out.println("alunos no cluster 1: " + cluster1.getStudents().size());
        System.out.println("alunos no cluster 2: " + cluster2.getStudents().size());
        System.out.println("alunos no cluster 3: " + cluster3.getStudents().size());

    }
}