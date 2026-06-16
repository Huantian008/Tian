package com.ywt.sms.controller;

import com.ywt.sms.common.ApiResponse;
import com.ywt.sms.mapper.DashboardMapper;
import com.ywt.sms.mapper.ScoreMapper;
import com.ywt.sms.model.DashboardSummary;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/dashboard")
public class DashboardController {
    private final DashboardMapper dashboardMapper;
    private final ScoreMapper scoreMapper;

    public DashboardController(DashboardMapper dashboardMapper, ScoreMapper scoreMapper) {
        this.dashboardMapper = dashboardMapper;
        this.scoreMapper = scoreMapper;
    }

    @GetMapping("/summary")
    public ApiResponse<DashboardSummary> summary() {
        return ApiResponse.ok(new DashboardSummary(
                dashboardMapper.countStudents(),
                dashboardMapper.countCourses(),
                scoreMapper.countAll(),
                Math.round(scoreMapper.averageScore() * 10.0) / 10.0
        ));
    }
}

