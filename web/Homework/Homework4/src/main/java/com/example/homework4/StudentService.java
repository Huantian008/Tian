package com.example.homework4;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class StudentService {
    private Student student;

    @Autowired
    public void setStudent(Student student) {
        this.student = student;
    }

    public void printStudentInfo() {
        System.out.println("StudentService.printStudentInfo(): " + student);
    }
}
