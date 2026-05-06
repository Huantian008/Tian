package com.example.homework6.controller;

import com.example.homework6.model.Student;
import com.example.homework6.service.StudentService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/students")
public class StudentController {
    private final StudentService studentService;

    public StudentController(StudentService studentService) {
        this.studentService = studentService;
    }

    @GetMapping
    public String list(Model model) {
        model.addAttribute("student", new Student());
        model.addAttribute("students", studentService.findAllStudents());
        return "students";
    }

    @PostMapping("/save")
    public String save(@ModelAttribute Student student, RedirectAttributes redirectAttributes) {
        boolean success = studentService.saveStudent(student);
        redirectAttributes.addFlashAttribute("message", success ? "学生保存成功" : "学生保存失败");
        return "redirect:/students";
    }

    @PostMapping("/update")
    public String update(@ModelAttribute Student student, RedirectAttributes redirectAttributes) {
        boolean success = studentService.updateStudent(student);
        redirectAttributes.addFlashAttribute("message", success ? "学生修改成功" : "学生修改失败");
        return "redirect:/students";
    }

    @PostMapping("/delete")
    public String delete(@RequestParam("id") Integer id, RedirectAttributes redirectAttributes) {
        boolean success = studentService.deleteStudent(id);
        redirectAttributes.addFlashAttribute("message", success ? "学生删除成功" : "学生删除失败");
        return "redirect:/students";
    }
}
