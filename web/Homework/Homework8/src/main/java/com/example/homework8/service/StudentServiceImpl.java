package com.example.homework8.service;

import com.example.homework8.mapper.StudentMapper;
import com.example.homework8.model.Student;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class StudentServiceImpl implements StudentService {
    private final StudentMapper studentMapper;

    public StudentServiceImpl(StudentMapper studentMapper) {
        this.studentMapper = studentMapper;
    }

    @Override
    @Transactional
    public boolean addStudent(Student student) {
        return studentMapper.insert(student) > 0;
    }

    @Override
    @Transactional
    public boolean updateStudent(Student student) {
        return studentMapper.update(student) > 0;
    }

    @Override
    @Transactional
    public boolean deleteStudent(Integer id) {
        return studentMapper.deleteById(id) > 0;
    }

    @Override
    public Student findStudentById(Integer id) {
        return studentMapper.findById(id);
    }

    @Override
    public List<Student> findStudentsByName(String name) {
        return studentMapper.findByNameLike(name);
    }

    @Override
    public List<Student> searchStudents(String name, String address) {
        return studentMapper.searchByNameAndAddress(name, address);
    }

    @Override
    public List<Student> findAllStudents() {
        return studentMapper.findAll();
    }
}
