package javawork4;

public abstract class Vegetable {
    public abstract void reapMethod();

    public abstract void cook();

    public static void main(String[] args) {
        Vegetable cabbage = new LeafyVegetable("cabbage");
        cabbage.reapMethod();
        cabbage.cook();
    }

    private static final class LeafyVegetable extends Vegetable {
        private final String name;

        private LeafyVegetable(String name) {
            this.name = name;
        }

        @Override
        public void reapMethod() {
            System.out.println("Harvest " + name + " by cutting near the base.");
        }

        @Override
        public void cook() {
            System.out.println("Cook " + name + " quickly with garlic and oil.");
        }
    }
}
