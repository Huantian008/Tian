package com.ywt.sms.mapper;

import com.ywt.sms.model.Student;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface StudentMapper {
    @Select("""
            select id, student_no, name, gender, age, class_name, major, phone, email
            from student
            where (#{keyword} is null or #{keyword} = ''
              or student_no like concat('%', #{keyword}, '%')
              or name like concat('%', #{keyword}, '%')
              or class_name like concat('%', #{keyword}, '%'))
            order by id desc
            limit #{limit} offset #{offset}
            """)
    List<Student> findPage(String keyword, int limit, int offset);

    @Select("""
            select count(1)
            from student
            where (#{keyword} is null or #{keyword} = ''
              or student_no like concat('%', #{keyword}, '%')
              or name like concat('%', #{keyword}, '%')
              or class_name like concat('%', #{keyword}, '%'))
            """)
    long count(String keyword);

    @Select("select id, student_no, name, gender, age, class_name, major, phone, email from student order by student_no")
    List<Student> findAll();

    @Insert("""
            insert into student(student_no, name, gender, age, class_name, major, phone, email)
            values(#{studentNo}, #{name}, #{gender}, #{age}, #{className}, #{major}, #{phone}, #{email})
            """)
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Student student);

    @Update("""
            update student set student_no=#{studentNo}, name=#{name}, gender=#{gender}, age=#{age},
            class_name=#{className}, major=#{major}, phone=#{phone}, email=#{email}
            where id=#{id}
            """)
    int update(Student student);

    @Delete("delete from student where id=#{id}")
    int delete(Long id);
}

