package legacy.basics.test;

import java.util.Scanner;

public class Employee {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("第一个数字");
        double num1 = scanner.nextDouble();
        System.out.println("two");
        double num2 = scanner.nextDouble();
        char jisuan = scanner.next().charAt(0);
        double recult;
        switch (jisuan) {
            case '+':
                recult = num1 + num2;
                break;
            case '-':
                recult = num1 - num2;
                break;
            case '*':
                recult = num1 * num2;
                break;
            case '/':
                if (num2 != 0) {
                    recult = num1 / num2;
                } else {
                    System.out.println("除数不为零");
                    return;
                }
                break;
            default:
                System.out.println("操作出错");
                return;
        }
        System.out.printf("结果:%2f", recult);
    }
}
