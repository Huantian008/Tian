package com.ywt.sms.model;

import jakarta.validation.constraints.NotNull;

public class Score {
    private Long id;
    @NotNull(message = "学生不能为空")
    private Long studentId;
    @NotNull(message = "课程不能为空")
    private Long courseId;
    private Double score;
    private String semester;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getStudentId() { return studentId; }
    public void setStudentId(Long studentId) { this.studentId = studentId; }
    public Long getCourseId() { return courseId; }
    public void setCourseId(Long courseId) { this.courseId = courseId; }
    public Double getScore() { return score; }
    public void setScore(Double score) { this.score = score; }
    public String getSemester() { return semester; }
    public void setSemester(String semester) { this.semester = semester; }
}

