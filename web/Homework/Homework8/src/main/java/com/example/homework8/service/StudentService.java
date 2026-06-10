package com.example.homework8.service;

import com.example.homework8.model.Student;

import java.util.List;

public interface StudentService {
    boolean addStudent(Student student);

    boolean updateStudent(Student student);

    boolean deleteStudent(Integer id);

    Student findStudentById(Integer id);

    List<Student> findStudentsByName(String name);

    List<Student> searchStudents(String name, String address);

    List<Student> findAllStudents();
}
