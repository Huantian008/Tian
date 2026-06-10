package com.example.homework9.controller;

import com.example.homework9.model.Student;
import com.example.homework9.service.AdminService;
import com.example.homework9.service.StudentService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import javax.servlet.http.HttpSession;
import java.util.List;

@Controller
public class StudentController {
    private final AdminService adminService;
    private final StudentService studentService;

    public StudentController(AdminService adminService, StudentService studentService) {
        this.adminService = adminService;
        this.studentService = studentService;
    }

    @GetMapping("/")
    public String index() {
        return "redirect:/login";
    }

    @GetMapping("/login")
    public String loginPage() {
        return "login";
    }

    @PostMapping("/login")
    public String login(@RequestParam("username") String username,
                        @RequestParam("password") String password,
                        HttpSession session,
                        Model model) {
        if (adminService.login(username, password)) {
            session.setAttribute("loginUser", username);
            return "redirect:/students";
        }
        model.addAttribute("message", "用户名或密码错误");
        return "login";
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate();
        return "redirect:/login";
    }

    @GetMapping("/students")
    public String list(HttpSession session, Model model) {
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }
        model.addAttribute("students", studentService.findAll());
        return "students";
    }

    @GetMapping("/students/add")
    public String addPage(HttpSession session) {
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }
        return "student_form";
    }

    @PostMapping("/students/add")
    public String add(@ModelAttribute Student student, HttpSession session) {
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }
        studentService.add(student);
        return "redirect:/students";
    }

    @GetMapping("/students/edit")
    public String editPage(@RequestParam("id") Integer id, HttpSession session, Model model) {
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }
        model.addAttribute("student", studentService.findById(id));
        return "student_edit";
    }

    @PostMapping("/students/edit")
    public String edit(@ModelAttribute Student student, HttpSession session) {
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }
        studentService.update(student);
        return "redirect:/students";
    }

    @GetMapping("/students/delete")
    public String delete(@RequestParam("id") Integer id, HttpSession session) {
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }
        studentService.delete(id);
        return "redirect:/students";
    }

    @GetMapping("/students/search")
    public String search(@RequestParam(value = "keyword", required = false) String keyword,
                         HttpSession session,
                         Model model) {
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }
        List<Student> students = studentService.search(keyword);
        model.addAttribute("students", students);
        model.addAttribute("keyword", keyword);
        return "students";
    }

    private boolean isLoggedIn(HttpSession session) {
        return session != null && session.getAttribute("loginUser") != null;
    }
}
