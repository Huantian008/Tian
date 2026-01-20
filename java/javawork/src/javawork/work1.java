package javawork;

public class work1 {
    public static void main(String[] args) {
        int number = 496;
        int sum = 1; // 1 is always a proper divisor

        for (int i = 2; i * i <= number; i++) {
            if (number % i == 0) {
                sum += i;
                int paired = number / i;
                if (paired != i) {
                    sum += paired;
                }
            }
        }

        if (sum == number) {
            System.out.println(number + " is a perfect number.");
        } else {
            System.out.println(number + " is not a perfect number.");
        }
    }
}
