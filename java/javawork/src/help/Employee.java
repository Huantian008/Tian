package help;

public class Employee {
    private String name;
    private String title;

    public Employee() {
        this("Default Name", "Technical Director");
    }

    public Employee(String name, String title) {
        this.name = name;
        this.title = title;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void showInfo() {
        System.out.println("Name: " + name);
        System.out.println("Title: " + title);
    }
}
