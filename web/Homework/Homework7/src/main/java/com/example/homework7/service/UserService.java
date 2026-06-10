package com.example.homework7.service;

import com.example.homework7.model.User;

public interface UserService {
    User findByUsername(String username);

    User updateUser(User user);
}
