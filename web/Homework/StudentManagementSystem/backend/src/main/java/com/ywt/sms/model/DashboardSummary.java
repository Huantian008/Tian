package com.ywt.sms.model;

public class DashboardSummary {
    private long studentCount;
    private long courseCount;
    private long scoreCount;
    private double averageScore;

    public DashboardSummary(long studentCount, long courseCount, long scoreCount, double averageScore) {
        this.studentCount = studentCount;
        this.courseCount = courseCount;
        this.scoreCount = scoreCount;
        this.averageScore = averageScore;
    }

    public long getStudentCount() { return studentCount; }
    public void setStudentCount(long studentCount) { this.studentCount = studentCount; }
    public long getCourseCount() { return courseCount; }
    public void setCourseCount(long courseCount) { this.courseCount = courseCount; }
    public long getScoreCount() { return scoreCount; }
    public void setScoreCount(long scoreCount) { this.scoreCount = scoreCount; }
    public double getAverageScore() { return averageScore; }
    public void setAverageScore(double averageScore) { this.averageScore = averageScore; }
}

