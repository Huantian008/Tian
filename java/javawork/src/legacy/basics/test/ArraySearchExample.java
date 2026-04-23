package legacy.basics.test;

import java.util.Scanner;

public class ArraySearchExample {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("输入第一个数字：");
        double num1 = scanner.nextDouble();
        System.out.print("输入第二个数字：");
        double num2 = scanner.nextDouble();
        System.out.print("输入操作符（+，-，*，/）：");
        char operator = scanner.next().charAt(0);
        double result;
        switch (operator) {
            case '+':
                result = num1 + num2;
                break;
            case '-':
                result = num1 - num2;
                break;
            case '*':
                result = num1 * num2;
                break;
            case '/':
                if (num2 != 0) {
                    result = num1 / num2;
                } else {
                    System.out.println("除数不能为0");
                    return;
                }
                break;
            default:
                System.out.println("无效的操作符");
                return;
        }
        System.out.printf("结果：%2f", result);
    }
}
