package com.ywt.sms.controller;

import com.ywt.sms.common.ApiResponse;
import com.ywt.sms.dto.LoginRequest;
import com.ywt.sms.dto.LoginResponse;
import com.ywt.sms.mapper.AdminUserMapper;
import com.ywt.sms.model.AdminUser;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.UUID;

@RestController
@RequestMapping("/api/auth")
public class AuthController {
    private final AdminUserMapper adminUserMapper;

    public AuthController(AdminUserMapper adminUserMapper) {
        this.adminUserMapper = adminUserMapper;
    }

    @PostMapping("/login")
    public ApiResponse<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        AdminUser user = adminUserMapper.findByUsername(request.getUsername());
        if (user == null || !user.getPassword().equals(request.getPassword())) {
            return ApiResponse.fail("用户名或密码错误");
        }
        String token = "sms-" + UUID.randomUUID();
        return ApiResponse.ok(new LoginResponse(token, user.getUsername(), user.getRealName(), user.getRole()));
    }
}

