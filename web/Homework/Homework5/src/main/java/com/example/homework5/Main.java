package com.example.homework5;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class Main {
    public static void main(String[] args) {
        try (AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class)) {
            StudentService studentService = context.getBean(StudentService.class);

            System.out.println("=== Spring AOP 学生信息管理演示 ===");

            Student student = new Student("2026001", "张三", 20, "23计算机专升本7班");
            studentService.addStudent(student);

            Student queryStudent = studentService.getStudent("2026001");
            System.out.println("查询结果: " + queryStudent);

            Student updatedStudent = new Student("2026001", "张三", 21, "23计算机专升本7班");
            studentService.updateStudent(updatedStudent);

            studentService.deleteStudent("2026001");

            try {
                studentService.getStudent("9999999");
            } catch (IllegalArgumentException e) {
                System.out.println("业务层捕获异常: " + e.getMessage());
            }

            try {
                studentService.deleteStudent("");
            } catch (IllegalArgumentException e) {
                System.out.println("权限校验异常: " + e.getMessage());
            }
        }
    }
}
