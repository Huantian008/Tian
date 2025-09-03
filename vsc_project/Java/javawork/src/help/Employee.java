package help;

public class Employee {
    private String name;
    private String titlePos;

    // 无参构造方法
    public Employee() {
        this.name = "李彦宏";
        this.titlePos = "技术总监";
    }

    // 可为name和titlePos初始化的构造方法
    public Employee(String name, String titlePos) {
        this.name = name;
        this.titlePos = titlePos;
    }

    // 获取姓名
    public String getName() {
        return name;
    }

    // 设置姓名
    public void setName(String name) {
        this.name = name;
    }

    // 获取职称
    public String getTitlePos() {
        return titlePos;
    }

    // 设置职称
    public void setTitlePos(String titlePos) {
        this.titlePos = titlePos;
    }

    // 显示信息的方法
    public void showInfo() {
        System.out.println("姓名: " + name);
        System.out.println("职称: " + titlePos);
    }
}


