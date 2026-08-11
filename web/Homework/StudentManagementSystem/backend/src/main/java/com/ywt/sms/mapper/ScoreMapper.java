package com.ywt.sms.mapper;

import com.ywt.sms.model.Score;
import com.ywt.sms.model.ScoreView;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface ScoreMapper {
    @Select("""
            select sc.id, sc.student_id, sc.course_id, sc.score, sc.semester,
                   st.student_no, st.name as student_name, co.course_no, co.course_name
            from score sc
            join student st on sc.student_id = st.id
            join course co on sc.course_id = co.id
            where (#{keyword} is null or #{keyword} = ''
              or st.student_no like concat('%', #{keyword}, '%')
              or st.name like concat('%', #{keyword}, '%')
              or co.course_name like concat('%', #{keyword}, '%'))
            order by sc.id desc
            limit #{limit} offset #{offset}
            """)
    List<ScoreView> findPage(String keyword, int limit, int offset);

    @Select("""
            select count(1)
            from score sc
            join student st on sc.student_id = st.id
            join course co on sc.course_id = co.id
            where (#{keyword} is null or #{keyword} = ''
              or st.student_no like concat('%', #{keyword}, '%')
              or st.name like concat('%', #{keyword}, '%')
              or co.course_name like concat('%', #{keyword}, '%'))
            """)
    long count(String keyword);

    @Insert("insert into score(student_id, course_id, score, semester) values(#{studentId}, #{courseId}, #{score}, #{semester})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Score score);

    @Update("update score set student_id=#{studentId}, course_id=#{courseId}, score=#{score}, semester=#{semester} where id=#{id}")
    int update(Score score);

    @Delete("delete from score where id=#{id}")
    int delete(Long id);

    @Select("select count(1) from score")
    long countAll();

    @Select("select coalesce(avg(score), 0) from score")
    double averageScore();
}

