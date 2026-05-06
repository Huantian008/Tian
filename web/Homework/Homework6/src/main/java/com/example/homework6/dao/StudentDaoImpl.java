package com.example.homework6.dao;

import com.example.homework6.model.Student;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class StudentDaoImpl implements StudentDao {
    private final JdbcTemplate jdbcTemplate;

    public StudentDaoImpl(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Override
    public int save(Student student) {
        String sql = "INSERT INTO student (student_no, name, age, class_name) VALUES (?, ?, ?, ?)";
        return jdbcTemplate.update(sql, student.getStudentNo(), student.getName(), student.getAge(), student.getClassName());
    }

    @Override
    public int update(Student student) {
        String sql = "UPDATE student SET name = ?, age = ?, class_name = ? WHERE id = ?";
        return jdbcTemplate.update(sql, student.getName(), student.getAge(), student.getClassName(), student.getId());
    }

    @Override
    public int deleteById(Integer id) {
        String sql = "DELETE FROM student WHERE id = ?";
        return jdbcTemplate.update(sql, id);
    }

    @Override
    public Student findByStudentNo(String studentNo) {
        String sql = "SELECT id, student_no AS studentNo, name, age, class_name AS className FROM student WHERE student_no = ?";
        try {
            return jdbcTemplate.queryForObject(sql, new BeanPropertyRowMapper<Student>(Student.class), studentNo);
        } catch (EmptyResultDataAccessException e) {
            return null;
        }
    }

    @Override
    public List<Student> findAll() {
        String sql = "SELECT id, student_no AS studentNo, name, age, class_name AS className FROM student ORDER BY id";
        return jdbcTemplate.query(sql, new BeanPropertyRowMapper<Student>(Student.class));
    }
}
