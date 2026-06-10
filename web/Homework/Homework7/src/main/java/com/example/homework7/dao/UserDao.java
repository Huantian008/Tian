package com.example.homework7.dao;

import com.example.homework7.model.User;

public interface UserDao {
    User findByUsername(String username);

    User findById(Integer id);

    int update(User user);
}
