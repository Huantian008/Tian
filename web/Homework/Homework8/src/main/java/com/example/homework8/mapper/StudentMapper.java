package com.example.homework8.mapper;

import com.example.homework8.model.Student;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface StudentMapper {
    int insert(Student student);

    int update(Student student);

    int deleteById(@Param("id") Integer id);

    Student findById(@Param("id") Integer id);

    List<Student> findByNameLike(@Param("name") String name);

    List<Student> searchByNameAndAddress(@Param("name") String name, @Param("address") String address);

    List<Student> findAll();
}
