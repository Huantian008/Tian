package pack3;

import pack1.A;
import pack2.B;

public class c {
    public static void main(String[] args) {
        int sum = A.add(30);
        System.out.println("Sum of numbers 1..30 = " + sum);

        int factorialResult = B.cheng(10);
        System.out.println("10! = " + factorialResult);
    }
}
