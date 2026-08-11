package com.ywt.sms.model;

import jakarta.validation.constraints.NotBlank;

public class Student {
    private Long id;
    @NotBlank(message = "学号不能为空")
    private String studentNo;
    @NotBlank(message = "姓名不能为空")
    private String name;
    private String gender;
    private Integer age;
    private String className;
    private String major;
    private String phone;
    private String email;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getStudentNo() { return studentNo; }
    public void setStudentNo(String studentNo) { this.studentNo = studentNo; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getGender() { return gender; }
    public void setGender(String gender) { this.gender = gender; }
    public Integer getAge() { return age; }
    public void setAge(Integer age) { this.age = age; }
    public String getClassName() { return className; }
    public void setClassName(String className) { this.className = className; }
    public String getMajor() { return major; }
    public void setMajor(String major) { this.major = major; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}

