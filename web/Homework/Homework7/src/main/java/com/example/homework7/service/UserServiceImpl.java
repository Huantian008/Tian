package com.example.homework7.service;

import com.example.homework7.dao.UserDao;
import com.example.homework7.model.User;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserServiceImpl implements UserService {
    private final UserDao userDao;

    public UserServiceImpl(UserDao userDao) {
        this.userDao = userDao;
    }

    @Override
    public User findByUsername(String username) {
        if (username == null || username.trim().isEmpty()) {
            return null;
        }
        return userDao.findByUsername(username.trim());
    }

    @Override
    @Transactional
    public User updateUser(User user) {
        if (user == null || user.getId() == null) {
            return null;
        }
        int rows = userDao.update(user);
        if (rows == 0) {
            return null;
        }
        return userDao.findById(user.getId());
    }
}
