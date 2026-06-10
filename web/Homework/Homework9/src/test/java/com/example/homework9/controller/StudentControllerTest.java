package com.example.homework9.controller;

import com.example.homework9.model.Student;
import com.example.homework9.service.AdminService;
import com.example.homework9.service.StudentService;
import org.junit.Test;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.servlet.view.InternalResourceViewResolver;

import java.util.Collections;

import static org.hamcrest.Matchers.equalTo;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.model;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;
import static org.springframework.test.web.servlet.setup.MockMvcBuilders.standaloneSetup;

public class StudentControllerTest {
    @Test
    public void loginSuccessRedirectsToStudents() throws Exception {
        AdminService adminService = mock(AdminService.class);
        StudentService studentService = mock(StudentService.class);
        when(adminService.login("admin", "123456")).thenReturn(true);

        mockMvc(adminService, studentService)
                .perform(post("/login").param("username", "admin").param("password", "123456"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/students"));
    }

    @Test
    public void loginFailureReturnsLoginPage() throws Exception {
        AdminService adminService = mock(AdminService.class);
        StudentService studentService = mock(StudentService.class);
        when(adminService.login("admin", "bad")).thenReturn(false);

        mockMvc(adminService, studentService)
                .perform(post("/login").param("username", "admin").param("password", "bad"))
                .andExpect(status().isOk())
                .andExpect(view().name("login"))
                .andExpect(model().attribute("message", "用户名或密码错误"));
    }

    @Test
    public void studentListRequiresLogin() throws Exception {
        mockMvc(mock(AdminService.class), mock(StudentService.class))
                .perform(get("/students"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/login"));
    }

    @Test
    public void studentListShowsStudentsAfterLogin() throws Exception {
        AdminService adminService = mock(AdminService.class);
        StudentService studentService = mock(StudentService.class);
        Student student = sampleStudent();
        when(studentService.findAll()).thenReturn(Collections.singletonList(student));

        mockMvc(adminService, studentService)
                .perform(get("/students").session(loggedInSession()))
                .andExpect(status().isOk())
                .andExpect(view().name("students"))
                .andExpect(model().attribute("students", equalTo(Collections.singletonList(student))));
    }

    @Test
    public void addUpdateDeleteAndSearchRoutesCallService() throws Exception {
        AdminService adminService = mock(AdminService.class);
        StudentService studentService = mock(StudentService.class);
        MockMvc mockMvc = mockMvc(adminService, studentService);
        MockHttpSession session = loggedInSession();

        mockMvc.perform(post("/students/add").session(session)
                        .param("studentNo", "2026001")
                        .param("name", "张三")
                        .param("gender", "男")
                        .param("age", "20")
                        .param("className", "23计算机专升本7班")
                        .param("phone", "13800138000"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/students"));
        verify(studentService).add(any(Student.class));

        mockMvc.perform(post("/students/edit").session(session)
                        .param("id", "1")
                        .param("studentNo", "2026001")
                        .param("name", "张三")
                        .param("gender", "男")
                        .param("age", "21")
                        .param("className", "23计算机专升本7班")
                        .param("phone", "13900000000"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/students"));
        verify(studentService).update(any(Student.class));

        mockMvc.perform(get("/students/delete").session(session).param("id", "1"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/students"));
        verify(studentService).delete(1);

        mockMvc.perform(get("/students/search").session(session).param("keyword", "张"))
                .andExpect(status().isOk())
                .andExpect(view().name("students"));
        verify(studentService).search("张");
    }

    private MockMvc mockMvc(AdminService adminService, StudentService studentService) {
        InternalResourceViewResolver resolver = new InternalResourceViewResolver();
        resolver.setPrefix("/WEB-INF/views/");
        resolver.setSuffix(".jsp");
        return standaloneSetup(new StudentController(adminService, studentService))
                .setViewResolvers(resolver)
                .build();
    }

    private MockHttpSession loggedInSession() {
        MockHttpSession session = new MockHttpSession();
        session.setAttribute("loginUser", "admin");
        return session;
    }

    private Student sampleStudent() {
        Student student = new Student();
        student.setId(1);
        student.setStudentNo("2026001");
        student.setName("张三");
        student.setGender("男");
        student.setAge(20);
        student.setClassName("23计算机专升本7班");
        student.setPhone("13800138000");
        return student;
    }
}
