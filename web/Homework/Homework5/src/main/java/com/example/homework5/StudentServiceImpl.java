package com.example.homework5;

import java.util.LinkedHashMap;
import java.util.Map;

import org.springframework.stereotype.Service;

@Service
public class StudentServiceImpl implements StudentService {
    private final Map<String, Student> students = new LinkedHashMap<>();

    @Override
    public void addStudent(Student student) {
        validateStudent(student);
        students.put(student.getStudentId(), student);
        System.out.println("添加学生信息: " + student);
    }

    @Override
    public void updateStudent(Student student) {
        validateStudent(student);
        if (!students.containsKey(student.getStudentId())) {
            throw new IllegalArgumentException("未找到要更新的学生: " + student.getStudentId());
        }
        students.put(student.getStudentId(), student);
        System.out.println("更新学生信息: " + student);
    }

    @Override
    public void deleteStudent(String studentId) {
        Student removedStudent = students.remove(studentId);
        if (removedStudent == null) {
            throw new IllegalArgumentException("未找到要删除的学生: " + studentId);
        }
        System.out.println("删除学生信息: " + removedStudent);
    }

    @Override
    public Student getStudent(String studentId) {
        Student student = students.get(studentId);
        if (student == null) {
            throw new IllegalArgumentException("未找到学生: " + studentId);
        }
        System.out.println("根据学号查询学生信息: " + studentId);
        return student;
    }

    private void validateStudent(Student student) {
        if (student == null || student.getStudentId() == null || student.getStudentId().trim().isEmpty()) {
            throw new IllegalArgumentException("学生信息和学号不能为空");
        }
    }
}
