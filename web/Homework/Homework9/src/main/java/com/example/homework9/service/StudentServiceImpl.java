package com.example.homework9.service;

import com.example.homework9.mapper.StudentMapper;
import com.example.homework9.model.Student;
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
    public List<Student> findAll() {
        return studentMapper.findAll();
    }

    @Override
    public List<Student> search(String keyword) {
        if (keyword == null || keyword.trim().isEmpty()) {
            return studentMapper.findAll();
        }
        return studentMapper.search(keyword.trim());
    }

    @Override
    public Student findById(Integer id) {
        return studentMapper.findById(id);
    }

    @Override
    @Transactional
    public void add(Student student) {
        studentMapper.insert(student);
    }

    @Override
    @Transactional
    public void update(Student student) {
        studentMapper.update(student);
    }

    @Override
    @Transactional
    public void delete(Integer id) {
        studentMapper.deleteById(id);
    }
}
