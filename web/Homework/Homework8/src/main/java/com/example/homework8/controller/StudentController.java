package com.example.homework8.controller;

import com.example.homework8.model.Student;
import com.example.homework8.service.StudentService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Controller
public class StudentController {
    private final StudentService studentService;

    public StudentController(StudentService studentService) {
        this.studentService = studentService;
    }

    @GetMapping({"/", "/students"})
    public String index(Model model) {
        model.addAttribute("student", new Student());
        model.addAttribute("students", studentService.findAllStudents());
        return "index";
    }

    @PostMapping("/students/add")
    public String add(@ModelAttribute Student student, RedirectAttributes redirectAttributes) {
        boolean success = studentService.addStudent(student);
        redirectAttributes.addFlashAttribute("message", success ? "学生添加成功" : "学生添加失败");
        return "redirect:/students";
    }

    @PostMapping("/students/update")
    public String update(@ModelAttribute Student student, RedirectAttributes redirectAttributes) {
        boolean success = studentService.updateStudent(student);
        redirectAttributes.addFlashAttribute("message", success ? "学生修改成功" : "学生修改失败");
        return "redirect:/students";
    }

    @PostMapping("/students/delete")
    public String delete(@RequestParam("id") Integer id, RedirectAttributes redirectAttributes) {
        boolean success = studentService.deleteStudent(id);
        redirectAttributes.addFlashAttribute("message", success ? "学生删除成功" : "学生删除失败");
        return "redirect:/students";
    }

    @RequestMapping("/students/search")
    public String search(@RequestParam(value = "searchType", required = false, defaultValue = "all") String searchType,
                         @RequestParam(value = "id", required = false) Integer id,
                         @RequestParam(value = "name", required = false) String name,
                         @RequestParam(value = "address", required = false) String address,
                         Model model) {
        List<Student> students;
        if ("id".equals(searchType) && id != null) {
            Student student = studentService.findStudentById(id);
            students = student == null ? Collections.<Student>emptyList() : Collections.singletonList(student);
        } else if ("name".equals(searchType)) {
            students = studentService.findStudentsByName(trimToNull(name));
        } else if ("nameAddress".equals(searchType)) {
            students = studentService.searchStudents(trimToNull(name), trimToNull(address));
        } else {
            students = studentService.findAllStudents();
        }

        model.addAttribute("student", new Student());
        model.addAttribute("students", students == null ? new ArrayList<Student>() : students);
        model.addAttribute("searchType", searchType);
        model.addAttribute("queryId", id);
        model.addAttribute("queryName", name);
        model.addAttribute("queryAddress", address);
        return "index";
    }

    private String trimToNull(String value) {
        if (value == null) {
            return null;
        }
        String trimmed = value.trim();
        return trimmed.isEmpty() ? null : trimmed;
    }
}
