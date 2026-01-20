package javawork;

public class Plant {
    private String name;
    private double price;

    public Plant(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public Plant() {
        this("Evergreen", 500);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public void showInfo() {
        System.out.println("Plant name: " + name);
        System.out.println("Plant price: " + price);
    }

    public static void main(String[] args) {
        Plant p1 = new Plant("Plant A", 100);
        Plant p2 = new Plant();
        System.out.println("p1 details:");
        p1.showInfo();
        System.out.println();
        System.out.println("p2 details:");
        p2.showInfo();
        p2.setPrice(1_000);
        System.out.println();
        System.out.println("p2 details after price update:");
        p2.showInfo();
    }
}
