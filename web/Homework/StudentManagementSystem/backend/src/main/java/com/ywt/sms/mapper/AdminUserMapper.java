package com.ywt.sms.mapper;

import com.ywt.sms.model.AdminUser;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface AdminUserMapper {
    @Select("select id, username, password, real_name, role from admin_user where username = #{username} limit 1")
    AdminUser findByUsername(String username);
}

