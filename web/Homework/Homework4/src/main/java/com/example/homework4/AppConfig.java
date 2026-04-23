package com.example.homework4;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.context.annotation.Scope;

@Configuration
@ComponentScan("com.example.homework4")
public class AppConfig {
    @Bean
    @Primary
    public Student annotationStudent() {
        return new Student("2026001", "张三", 20, "23计算机专升本7班");
    }

    @Bean
    @Scope("prototype")
    public Student prototypeStudent() {
        return new Student("2026002", "李四", 21, "23计算机专升本7班");
    }
}
