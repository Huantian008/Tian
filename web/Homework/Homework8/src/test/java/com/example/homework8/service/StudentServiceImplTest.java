package com.example.homework8.service;

import com.example.homework8.mapper.StudentMapper;
import com.example.homework8.model.Student;
import org.junit.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertSame;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

public class StudentServiceImplTest {
    @Test
    public void delegatesCreateUpdateDeleteAndListToMapper() {
        StudentMapper mapper = mock(StudentMapper.class);
        StudentService service = new StudentServiceImpl(mapper);
        Student student = sampleStudent();
        List<Student> students = Arrays.asList(student);

        when(mapper.insert(student)).thenReturn(1);
        when(mapper.update(student)).thenReturn(1);
        when(mapper.deleteById(1)).thenReturn(1);
        when(mapper.findAll()).thenReturn(students);

        assertEquals(true, service.addStudent(student));
        assertEquals(true, service.updateStudent(student));
        assertEquals(true, service.deleteStudent(1));
        assertSame(students, service.findAllStudents());
    }

    @Test
    public void delegatesAllSearchModesToMapper() {
        StudentMapper mapper = mock(StudentMapper.class);
        StudentService service = new StudentServiceImpl(mapper);
        Student student = sampleStudent();
        List<Student> students = Arrays.asList(student);

        when(mapper.findById(1)).thenReturn(student);
        when(mapper.findByNameLike("张")).thenReturn(students);
        when(mapper.searchByNameAndAddress("张", "北京")).thenReturn(students);

        assertSame(student, service.findStudentById(1));
        assertSame(students, service.findStudentsByName("张"));
        assertSame(students, service.searchStudents("张", "北京"));
    }

    private Student sampleStudent() {
        Student student = new Student();
        student.setId(1);
        student.setName("张三");
        student.setAge(20);
        student.setSex("男");
        student.setAddress("北京市海淀区");
        return student;
    }
}
