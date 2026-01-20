package javatest;

public class E {
    public static void main(String[] args) {
        Account account = new Account("622600012010", "Alice", 6_000.0);
        account.display();

        Account defaultAccount = new Account();
        defaultAccount.display();
    }
}
