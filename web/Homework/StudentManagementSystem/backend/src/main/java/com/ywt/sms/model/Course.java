package com.ywt.sms.model;

import jakarta.validation.constraints.NotBlank;

public class Course {
    private Long id;
    @NotBlank(message = "课程编号不能为空")
    private String courseNo;
    @NotBlank(message = "课程名称不能为空")
    private String courseName;
    private Double credit;
    private String teacher;
    private String semester;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getCourseNo() { return courseNo; }
    public void setCourseNo(String courseNo) { this.courseNo = courseNo; }
    public String getCourseName() { return courseName; }
    public void setCourseName(String courseName) { this.courseName = courseName; }
    public Double getCredit() { return credit; }
    public void setCredit(Double credit) { this.credit = credit; }
    public String getTeacher() { return teacher; }
    public void setTeacher(String teacher) { this.teacher = teacher; }
    public String getSemester() { return semester; }
    public void setSemester(String semester) { this.semester = semester; }
}

