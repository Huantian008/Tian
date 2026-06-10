package com.example.homework9.service;

import com.example.homework9.model.Student;

import java.util.List;

public interface StudentService {
    List<Student> findAll();

    List<Student> search(String keyword);

    Student findById(Integer id);

    void add(Student student);

    void update(Student student);

    void delete(Integer id);
}
