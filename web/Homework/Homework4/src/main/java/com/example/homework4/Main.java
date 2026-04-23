package com.example.homework4;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class Main {
    public static void main(String[] args) {
        runAnnotationConfigDemo();
        System.out.println();
        runXmlConfigDemo();
    }

    private static void runAnnotationConfigDemo() {
        try (AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class)) {
            System.out.println("=== 注解方式管理 Bean ===");

            Student annotationStudent = context.getBean("annotationStudent", Student.class);
            System.out.println("构造器注入的 Student: " + annotationStudent);

            StudentService studentService = context.getBean(StudentService.class);
            studentService.printStudentInfo();

            Student singletonStudent1 = context.getBean("annotationStudent", Student.class);
            Student singletonStudent2 = context.getBean("annotationStudent", Student.class);
            System.out.println("singleton 两次获取是否为同一对象: " + (singletonStudent1 == singletonStudent2));

            Student prototypeStudent1 = context.getBean("prototypeStudent", Student.class);
            Student prototypeStudent2 = context.getBean("prototypeStudent", Student.class);
            System.out.println("prototype 两次获取是否为同一对象: " + (prototypeStudent1 == prototypeStudent2));
        }
    }

    private static void runXmlConfigDemo() {
        try (ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("applicationContext.xml")) {
            System.out.println("=== XML 方式管理 Bean ===");

            Student xmlStudent = context.getBean("xmlStudent", Student.class);
            System.out.println("Setter 注入的 Student: " + xmlStudent);

            Student xmlSingleton1 = context.getBean("xmlStudent", Student.class);
            Student xmlSingleton2 = context.getBean("xmlStudent", Student.class);
            System.out.println("XML singleton 两次获取是否为同一对象: " + (xmlSingleton1 == xmlSingleton2));

            Student xmlPrototype1 = context.getBean("xmlPrototypeStudent", Student.class);
            Student xmlPrototype2 = context.getBean("xmlPrototypeStudent", Student.class);
            System.out.println("XML prototype 两次获取是否为同一对象: " + (xmlPrototype1 == xmlPrototype2));
        }
    }
}
