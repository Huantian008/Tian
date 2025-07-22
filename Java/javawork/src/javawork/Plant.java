package javawork;

public class Plant {
    private String name;
    private double price;

    public Plant(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public Plant() {
        this("乔木", 500);
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
        System.out.println("植物名称: " + name);
        System.out.println("植物价格: " + price);
    }

    public static void main(String[] args) {
        Plant p1 = new Plant("植物1", 100);
        Plant p2 = new Plant();
        System.out.println("p1的信息：");
        p1.showInfo();
        System.out.println("\np2的信息：");
        p2.showInfo();
        p2.setPrice(1000);
        System.out.println("\n修改后p2的信息：");
        p2.showInfo();
    }
}
