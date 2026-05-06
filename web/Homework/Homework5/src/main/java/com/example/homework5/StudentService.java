package com.example.homework5;

public interface StudentService {
    void addStudent(Student student);

    void updateStudent(Student student);

    void deleteStudent(String studentId);

    Student getStudent(String studentId);
}
