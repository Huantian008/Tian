package javawork;

public class work2 {
    public static void main(String[] args) {
        int limit = 9_999;
        int n = 1;
        int factorial = 1;
        int sum = 0;

        while (sum + factorial <= limit) {
            sum += factorial;
            n++;
            factorial *= n;
        }

        System.out.println("Largest n with factorial sum <= " + limit + ": " + (n - 1));
        System.out.println("Factorial sum: " + sum);
    }
}
