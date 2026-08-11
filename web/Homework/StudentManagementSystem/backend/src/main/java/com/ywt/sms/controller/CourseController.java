package com.ywt.sms.controller;

import com.ywt.sms.common.ApiResponse;
import com.ywt.sms.common.PageResult;
import com.ywt.sms.mapper.CourseMapper;
import com.ywt.sms.model.Course;
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
@RequestMapping("/api/courses")
public class CourseController {
    private final CourseMapper courseMapper;

    public CourseController(CourseMapper courseMapper) {
        this.courseMapper = courseMapper;
    }

    @GetMapping
    public ApiResponse<PageResult<Course>> page(@RequestParam(defaultValue = "") String keyword,
                                                @RequestParam(defaultValue = "1") int page,
                                                @RequestParam(defaultValue = "10") int size) {
        int offset = Math.max(page - 1, 0) * size;
        return ApiResponse.ok(new PageResult<>(courseMapper.findPage(keyword, size, offset), courseMapper.count(keyword)));
    }

    @GetMapping("/all")
    public ApiResponse<List<Course>> all() {
        return ApiResponse.ok(courseMapper.findAll());
    }

    @PostMapping
    public ApiResponse<Course> create(@Valid @RequestBody Course course) {
        courseMapper.insert(course);
        return ApiResponse.ok(course);
    }

    @PutMapping("/{id}")
    public ApiResponse<Course> update(@PathVariable Long id, @Valid @RequestBody Course course) {
        course.setId(id);
        courseMapper.update(course);
        return ApiResponse.ok(course);
    }

    @DeleteMapping("/{id}")
    public ApiResponse<Void> delete(@PathVariable Long id) {
        courseMapper.delete(id);
        return ApiResponse.ok(null);
    }
}

