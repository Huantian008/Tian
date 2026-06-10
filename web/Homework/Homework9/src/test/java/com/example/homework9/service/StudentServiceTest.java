package com.example.homework9.service;

import com.example.homework9.mapper.StudentMapper;
import com.example.homework9.model.Student;
import org.junit.Test;

import java.util.Collections;
import java.util.List;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.equalTo;
import static org.junit.Assert.assertSame;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

public class StudentServiceTest {
    @Test
    public void listReturnsAllStudents() {
        StudentMapper mapper = mock(StudentMapper.class);
        List<Student> students = Collections.singletonList(sampleStudent());
        when(mapper.findAll()).thenReturn(students);

        StudentService service = new StudentServiceImpl(mapper);

        assertSame(students, service.findAll());
    }

    @Test
    public void searchDelegatesKeywordToMapper() {
        StudentMapper mapper = mock(StudentMapper.class);
        List<Student> students = Collections.singletonList(sampleStudent());
        when(mapper.search("张")).thenReturn(students);

        StudentService service = new StudentServiceImpl(mapper);

        assertThat(service.search("张"), equalTo(students));
    }

    @Test
    public void addUpdateAndDeleteUseMapper() {
        StudentMapper mapper = mock(StudentMapper.class);
        StudentService service = new StudentServiceImpl(mapper);
        Student student = sampleStudent();

        service.add(student);
        service.update(student);
        service.delete(1);

        verify(mapper).insert(student);
        verify(mapper).update(student);
        verify(mapper).deleteById(1);
    }

    private Student sampleStudent() {
        Student student = new Student();
        student.setId(1);
        student.setStudentNo("2026001");
        student.setName("张三");
        student.setGender("男");
        student.setAge(20);
        student.setClassName("23计算机专升本7班");
        student.setPhone("13800138000");
        return student;
    }
}
