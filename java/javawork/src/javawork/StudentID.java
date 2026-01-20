package javawork;

import java.util.Arrays;
import java.util.Scanner;

public class StudentID {
    public static void main(String[] args) {
        try (Scanner input = new Scanner(System.in)) {
            String[] studentIds = new String[5];
            for (int i = 0; i < studentIds.length; i++) {
                System.out.print("Enter student ID #" + (i + 1) + " (should start with 2023): ");
                studentIds[i] = input.nextLine();
            }

            System.out.println();
            System.out.println("Collected student IDs:");
            System.out.println(Arrays.toString(studentIds));
        }
    }
}
