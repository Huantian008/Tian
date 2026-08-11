package com.ywt.sms.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface DashboardMapper {
    @Select("select count(1) from student")
    long countStudents();

    @Select("select count(1) from course")
    long countCourses();
}

