package javawork3;

public class Building {
    private String name;
    private String style;

    public Building() {
        this("Bird's Nest", "Modern");
    }

    public Building(String name, String style) {
        this.name = name;
        this.style = style;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setStyle(String style) {
        this.style = style;
    }

    public String getStyle() {
        return style;
    }

    public void introduce() {
        System.out.println("This building is called " + name + ".");
        System.out.println("Architectural style: " + style + ".");
    }
}
