package com.example.homework6.service;

import com.example.homework6.model.Student;

import java.util.List;

public interface StudentService {
    boolean saveStudent(Student student);

    boolean updateStudent(Student student);

    boolean deleteStudent(Integer id);

    Student findStudentByNo(String studentNo);

    List<Student> findAllStudents();
}
