package com.example.homework9.mapper;

import com.example.homework9.model.AdminUser;

public interface AdminUserMapper {
    AdminUser findByUsername(String username);
}
