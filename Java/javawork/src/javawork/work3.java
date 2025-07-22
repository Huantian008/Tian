package javawork;

import java.util.Scanner;

public class work3 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("请输入月份（1-12）：");
        int month = scanner.nextInt();

        switch (month) {
            case 1:
                System.out.println("1月的天数是31天");
                break;
            case 2:
                System.out.println("2月的天数是28或29天");
                break;
            case 3:
                System.out.println("3月的天数是31天");
                break;
            case 4:
                System.out.println("4月的天数是30天");
                break;
            case 5:
                System.out.println("5月的天数是31天");
                break;
            case 6:
                System.out.println("6月的天数是30天");
                break;
            case 7:
                System.out.println("7月的天数是31天");
                break;
            case 8:
                System.out.println("8月的天数是31天");
                break;
            case 9:
                System.out.println("9月的天数是30天");
                break;
            case 10:
                System.out.println("10月的天数是31天");
                break;
            case 11:
                System.out.println("11月的天数是30天");
                break;
            case 12:
                System.out.println("12月的天数是31天");
                break;
            default:
                System.out.println("输入无效，月份应在1-12之间");
        }
    }
}
