package com.ywt.sms.mapper;

import com.ywt.sms.model.Course;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface CourseMapper {
    @Select("""
            select id, course_no, course_name, credit, teacher, semester
            from course
            where (#{keyword} is null or #{keyword} = ''
              or course_no like concat('%', #{keyword}, '%')
              or course_name like concat('%', #{keyword}, '%')
              or teacher like concat('%', #{keyword}, '%'))
            order by id desc
            limit #{limit} offset #{offset}
            """)
    List<Course> findPage(String keyword, int limit, int offset);

    @Select("""
            select count(1)
            from course
            where (#{keyword} is null or #{keyword} = ''
              or course_no like concat('%', #{keyword}, '%')
              or course_name like concat('%', #{keyword}, '%')
              or teacher like concat('%', #{keyword}, '%'))
            """)
    long count(String keyword);

    @Select("select id, course_no, course_name, credit, teacher, semester from course order by course_no")
    List<Course> findAll();

    @Insert("""
            insert into course(course_no, course_name, credit, teacher, semester)
            values(#{courseNo}, #{courseName}, #{credit}, #{teacher}, #{semester})
            """)
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Course course);

    @Update("""
            update course set course_no=#{courseNo}, course_name=#{courseName}, credit=#{credit},
            teacher=#{teacher}, semester=#{semester}
            where id=#{id}
            """)
    int update(Course course);

    @Delete("delete from course where id=#{id}")
    int delete(Long id);
}

