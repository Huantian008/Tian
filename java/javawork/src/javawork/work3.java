package javawork;

import java.util.Map;
import java.util.Scanner;

public class work3 {
    private static final Map<Integer, String> MONTH_TO_DAYS = Map.ofEntries(
            Map.entry(1, "31 days"),
            Map.entry(2, "28 or 29 days"),
            Map.entry(3, "31 days"),
            Map.entry(4, "30 days"),
            Map.entry(5, "31 days"),
            Map.entry(6, "30 days"),
            Map.entry(7, "31 days"),
            Map.entry(8, "31 days"),
            Map.entry(9, "30 days"),
            Map.entry(10, "31 days"),
            Map.entry(11, "30 days"),
            Map.entry(12, "31 days")
    );

    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            System.out.print("Enter a month number (1-12): ");
            if (!scanner.hasNextInt()) {
                System.out.println("Input must be an integer.");
                return;
            }

            int month = scanner.nextInt();
            String days = MONTH_TO_DAYS.get(month);
            if (days == null) {
                System.out.println("Month must be between 1 and 12.");
            } else {
                System.out.println("Month " + month + " has " + days + ".");
            }
        }
    }
}
