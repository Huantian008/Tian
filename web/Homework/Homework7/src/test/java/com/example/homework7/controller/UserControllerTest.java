package com.example.homework7.controller;

import com.example.homework7.model.User;
import com.example.homework7.service.UserService;
import org.junit.Test;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.servlet.view.InternalResourceViewResolver;

import static org.hamcrest.Matchers.equalTo;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.model;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;
import static org.springframework.test.web.servlet.setup.MockMvcBuilders.standaloneSetup;

public class UserControllerTest {

    @Test
    public void queryUserBindsResultToEditForm() throws Exception {
        UserService userService = mock(UserService.class);
        User user = sampleUser();
        when(userService.findByUsername("zhangsan")).thenReturn(user);

        MockMvc mockMvc = mockMvc(userService);

        mockMvc.perform(post("/user/find").param("username", "zhangsan"))
                .andExpect(status().isOk())
                .andExpect(view().name("edit"))
                .andExpect(model().attribute("user", equalTo(user)));
    }

    @Test
    public void queryMissingUserReturnsQueryPageWithMessage() throws Exception {
        UserService userService = mock(UserService.class);
        when(userService.findByUsername("missing")).thenReturn(null);

        MockMvc mockMvc = mockMvc(userService);

        mockMvc.perform(post("/user/find").param("username", "missing"))
                .andExpect(status().isOk())
                .andExpect(view().name("query"))
                .andExpect(model().attribute("message", "没有查询到用户：missing"));
    }

    @Test
    public void updateUserForwardsToShowPage() throws Exception {
        UserService userService = mock(UserService.class);
        User updated = sampleUser();
        updated.setPhone("13900000000");
        updated.setAddress("上海市浦东新区");
        when(userService.updateUser(org.mockito.ArgumentMatchers.any(User.class))).thenReturn(updated);

        MockMvc mockMvc = mockMvc(userService);

        mockMvc.perform(post("/user/update")
                        .param("id", "1")
                        .param("username", "zhangsan")
                        .param("password", "123456")
                        .param("realName", "张三")
                        .param("gender", "男")
                        .param("age", "20")
                        .param("phone", "13900000000")
                        .param("email", "zhangsan@example.com")
                        .param("address", "上海市浦东新区"))
                .andExpect(status().isOk())
                .andExpect(view().name("show"))
                .andExpect(model().attribute("user", equalTo(updated)))
                .andExpect(model().attribute("message", "用户信息修改成功"));
        verify(userService).updateUser(org.mockito.ArgumentMatchers.any(User.class));
    }

    @Test
    public void loginShowsWelcomeMessage() throws Exception {
        UserService userService = mock(UserService.class);
        User user = sampleUser();
        when(userService.findByUsername("zhangsan")).thenReturn(user);

        MockMvc mockMvc = mockMvc(userService);

        mockMvc.perform(post("/user/login").param("username", "zhangsan"))
                .andExpect(status().isOk())
                .andExpect(view().name("show"))
                .andExpect(model().attribute("user", equalTo(user)))
                .andExpect(model().attribute("message", "欢迎张三"));
    }

    @Test
    public void loginPageAndQueryPageRender() throws Exception {
        UserService userService = mock(UserService.class);
        MockMvc mockMvc = mockMvc(userService);

        mockMvc.perform(get("/user/login"))
                .andExpect(status().isOk())
                .andExpect(view().name("login"));
        mockMvc.perform(get("/user/query"))
                .andExpect(status().isOk())
                .andExpect(view().name("query"));
    }

    private User sampleUser() {
        User user = new User();
        user.setId(1);
        user.setUsername("zhangsan");
        user.setPassword("123456");
        user.setRealName("张三");
        user.setGender("男");
        user.setAge(20);
        user.setPhone("13800138000");
        user.setEmail("zhangsan@example.com");
        user.setAddress("北京市海淀区");
        return user;
    }

    private MockMvc mockMvc(UserService userService) {
        InternalResourceViewResolver resolver = new InternalResourceViewResolver();
        resolver.setPrefix("/WEB-INF/views/");
        resolver.setSuffix(".jsp");
        return standaloneSetup(new UserController(userService))
                .setViewResolvers(resolver)
                .build();
    }
}
