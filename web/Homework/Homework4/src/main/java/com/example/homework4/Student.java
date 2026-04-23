package com.example.homework4;

public class Student {
    private String id;
    private String name;
    private int age;
    private String classId;

    public Student() {
    }

    public Student(String id, String name, int age, String classId) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.classId = classId;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getClassId() {
        return classId;
    }

    public void setClassId(String classId) {
        this.classId = classId;
    }

    @Override
    public String toString() {
        return "Student{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", age=" + age +
                ", classId='" + classId + '\'' +
                '}';
    }
}
