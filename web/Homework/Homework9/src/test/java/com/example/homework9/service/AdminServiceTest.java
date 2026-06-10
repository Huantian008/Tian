package com.example.homework9.service;

import com.example.homework9.mapper.AdminUserMapper;
import com.example.homework9.model.AdminUser;
import org.junit.Test;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class AdminServiceTest {
    @Test
    public void loginSucceedsWhenUsernameAndPasswordMatch() {
        AdminUserMapper mapper = mock(AdminUserMapper.class);
        AdminUser user = new AdminUser();
        user.setUsername("admin");
        user.setPassword("123456");
        when(mapper.findByUsername("admin")).thenReturn(user);

        AdminService service = new AdminServiceImpl(mapper);

        assertTrue(service.login("admin", "123456"));
    }

    @Test
    public void loginFailsWhenPasswordDoesNotMatch() {
        AdminUserMapper mapper = mock(AdminUserMapper.class);
        AdminUser user = new AdminUser();
        user.setUsername("admin");
        user.setPassword("123456");
        when(mapper.findByUsername("admin")).thenReturn(user);

        AdminService service = new AdminServiceImpl(mapper);

        assertFalse(service.login("admin", "wrong"));
    }
}
