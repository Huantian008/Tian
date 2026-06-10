package com.example.homework9.service;

import com.example.homework9.mapper.AdminUserMapper;
import com.example.homework9.model.AdminUser;
import org.springframework.stereotype.Service;

@Service
public class AdminServiceImpl implements AdminService {
    private final AdminUserMapper adminUserMapper;

    public AdminServiceImpl(AdminUserMapper adminUserMapper) {
        this.adminUserMapper = adminUserMapper;
    }

    @Override
    public boolean login(String username, String password) {
        AdminUser adminUser = adminUserMapper.findByUsername(username);
        return adminUser != null && adminUser.getPassword() != null && adminUser.getPassword().equals(password);
    }
}
