package com.example.homework9.mapper;

import com.example.homework9.model.Student;

import java.util.List;

public interface StudentMapper {
    List<Student> findAll();

    List<Student> search(String keyword);

    Student findById(Integer id);

    int insert(Student student);

    int update(Student student);

    int deleteById(Integer id);
}
