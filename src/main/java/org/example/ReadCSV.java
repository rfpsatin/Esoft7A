package org.example;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class ReadCSV {

    public static List<Student> readCSV(String path) {
        try {
            List<String> lines = Files.readAllLines(Paths.get(path));
            return lines.stream().skip(1)
                    .map(line -> line.split(","))
                    .map((e) -> new Student(Integer.parseInt(e[1]),
                            Double.parseDouble(e[2]),
                            Double.parseDouble(e[3])))
                    .toList();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public String toString() {
        return "ReadCSV{}";
    }
}
