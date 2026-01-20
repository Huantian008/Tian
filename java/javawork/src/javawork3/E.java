package javawork3;

public class E {
    public static void main(String[] args) {
        Building defaultBuilding = new Building();
        defaultBuilding.introduce();

        Building museum = new Building("Louvre Pyramid", "Contemporary");
        museum.introduce();
    }
}
