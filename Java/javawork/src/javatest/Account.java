package javatest;

public class Account {
    private String accountNumber;
    private String name;
    private double balance;

    public Account(String accountNumber, String name, double balance) {
        this.accountNumber = accountNumber;
        this.name = name;
        this.balance = balance;
    }

    public Account() {
        this("622600012010", "张三丰", 6000.0);
    }

    public void setAccountNumber(String accountNumber) {
        this.accountNumber = accountNumber;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getBalance() {
        return balance;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }

    public void display() {
        System.out.println("账户:" + accountNumber);
        System.out.println("姓名:" + name);
        System.out.println("余额：" + balance);
    }
}
