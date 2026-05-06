package com.example.homework6.service;

import com.example.homework6.dao.StudentDao;
import com.example.homework6.model.Student;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StudentServiceImpl implements StudentService {
    private final StudentDao studentDao;

    public StudentServiceImpl(StudentDao studentDao) {
        this.studentDao = studentDao;
    }

    @Override
    public boolean saveStudent(Student student) {
        return studentDao.save(student) > 0;
    }

    @Override
    public boolean updateStudent(Student student) {
        return studentDao.update(student) > 0;
    }

    @Override
    public boolean deleteStudent(Integer id) {
        return studentDao.deleteById(id) > 0;
    }

    @Override
    public Student findStudentByNo(String studentNo) {
        return studentDao.findByStudentNo(studentNo);
    }

    @Override
    public List<Student> findAllStudents() {
        return studentDao.findAll();
    }
}
