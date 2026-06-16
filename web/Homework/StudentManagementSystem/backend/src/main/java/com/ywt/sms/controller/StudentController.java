package com.ywt.sms.controller;

import com.ywt.sms.common.ApiResponse;
import com.ywt.sms.common.PageResult;
import com.ywt.sms.mapper.StudentMapper;
import com.ywt.sms.model.Student;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/students")
public class StudentController {
    private final StudentMapper studentMapper;

    public StudentController(StudentMapper studentMapper) {
        this.studentMapper = studentMapper;
    }

    @GetMapping
    public ApiResponse<PageResult<Student>> page(@RequestParam(defaultValue = "") String keyword,
                                                 @RequestParam(defaultValue = "1") int page,
                                                 @RequestParam(defaultValue = "10") int size) {
        int offset = Math.max(page - 1, 0) * size;
        return ApiResponse.ok(new PageResult<>(studentMapper.findPage(keyword, size, offset), studentMapper.count(keyword)));
    }

    @GetMapping("/all")
    public ApiResponse<List<Student>> all() {
        return ApiResponse.ok(studentMapper.findAll());
    }

    @PostMapping
    public ApiResponse<Student> create(@Valid @RequestBody Student student) {
        studentMapper.insert(student);
        return ApiResponse.ok(student);
    }

    @PutMapping("/{id}")
    public ApiResponse<Student> update(@PathVariable Long id, @Valid @RequestBody Student student) {
        student.setId(id);
        studentMapper.update(student);
        return ApiResponse.ok(student);
    }

    @DeleteMapping("/{id}")
    public ApiResponse<Void> delete(@PathVariable Long id) {
        studentMapper.delete(id);
        return ApiResponse.ok(null);
    }
}

