package com.example.homework7.dao;

import com.example.homework7.model.User;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

@Repository
public class UserDaoImpl implements UserDao {
    private final JdbcTemplate jdbcTemplate;

    private final RowMapper<User> userRowMapper = (rs, rowNum) -> {
        User user = new User();
        user.setId(rs.getInt("id"));
        user.setUsername(rs.getString("username"));
        user.setPassword(rs.getString("password"));
        user.setRealName(rs.getString("real_name"));
        user.setGender(rs.getString("gender"));
        user.setAge(rs.getInt("age"));
        user.setPhone(rs.getString("phone"));
        user.setEmail(rs.getString("email"));
        user.setAddress(rs.getString("address"));
        return user;
    };

    public UserDaoImpl(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Override
    public User findByUsername(String username) {
        try {
            return jdbcTemplate.queryForObject(
                    "select id, username, password, real_name, gender, age, phone, email, address from user_info where username = ?",
                    userRowMapper,
                    username);
        } catch (EmptyResultDataAccessException e) {
            return null;
        }
    }

    @Override
    public User findById(Integer id) {
        try {
            return jdbcTemplate.queryForObject(
                    "select id, username, password, real_name, gender, age, phone, email, address from user_info where id = ?",
                    userRowMapper,
                    id);
        } catch (EmptyResultDataAccessException e) {
            return null;
        }
    }

    @Override
    public int update(User user) {
        return jdbcTemplate.update(
                "update user_info set username = ?, password = ?, real_name = ?, gender = ?, age = ?, phone = ?, email = ?, address = ? where id = ?",
                user.getUsername(),
                user.getPassword(),
                user.getRealName(),
                user.getGender(),
                user.getAge(),
                user.getPhone(),
                user.getEmail(),
                user.getAddress(),
                user.getId());
    }
}
