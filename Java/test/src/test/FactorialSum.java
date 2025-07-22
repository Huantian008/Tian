package test;

public class FactorialSum {public static void main(String[] args) {
    double sum = 1.0; // 初始和为1
    double factorial = 1.0;

    for (int i = 2; i <= 20; i++) {
        factorial *= i; // 计算i的阶乘
        sum += 1.0 / factorial; // 加上1/i!到和中
    }

    System.out.println("1 + 1/2! + 1/3! + 1/4! + ... + 1/20! = " + sum);
}

}
