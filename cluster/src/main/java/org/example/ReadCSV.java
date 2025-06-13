package org.example;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class ReadCSV {

    public static List<Student> readCSV(String path) {
        try {
            List<String> lines = Files.readAllLines(Paths.get(path));
            List<Student> students = lines.stream()
                    .skip(1)
                    .map(String::trim)
                    .filter(line -> !line.isBlank())
                    .map(line -> line.split(","))
                    .filter(e -> e.length == 5)
                    .map(e -> new Student(
                            Integer.parseInt(e[1].trim()),
                            Double.parseDouble(e[2].trim()),
                            Double.parseDouble(e[3].trim()),
                            e[4].trim())

                    )
                    .toList();

            List<String> allCategories = students.stream()
                    .map(Student::getCategory)
                    .distinct()
                    .sorted()
                    .toList();

            students.forEach(student -> student.encodeCourseCategory(allCategories));

            return students;

        } catch (IOException e) {
            throw new RuntimeException("Erro ao ler o arquivo CSV", e);
        }
    }

    @Override
    public String toString() {
        return "ReadCSV{}";
    }
}
