package com.example.homework6.dao;

import com.example.homework6.model.Student;

import java.util.List;

public interface StudentDao {
    int save(Student student);

    int update(Student student);

    int deleteById(Integer id);

    Student findByStudentNo(String studentNo);

    List<Student> findAll();
}
