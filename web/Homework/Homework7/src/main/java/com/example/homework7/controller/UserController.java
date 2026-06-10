package com.example.homework7.controller;

import com.example.homework7.model.User;
import com.example.homework7.service.UserService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
@RequestMapping("/user")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/login")
    public String loginPage() {
        return "login";
    }

    @PostMapping("/login")
    public String login(@RequestParam("username") String username, Model model) {
        User user = userService.findByUsername(username);
        if (user == null) {
            model.addAttribute("message", "登录失败，没有找到用户：" + username);
            return "login";
        }
        model.addAttribute("user", user);
        model.addAttribute("message", "欢迎" + user.getRealName());
        return "show";
    }

    @GetMapping("/query")
    public String queryPage() {
        return "query";
    }

    @PostMapping("/find")
    public String find(@RequestParam("username") String username, Model model) {
        User user = userService.findByUsername(username);
        if (user == null) {
            model.addAttribute("message", "没有查询到用户：" + username);
            return "query";
        }
        model.addAttribute("user", user);
        return "edit";
    }

    @PostMapping("/update")
    public String update(@ModelAttribute User user, Model model) {
        User updatedUser = userService.updateUser(user);
        if (updatedUser == null) {
            model.addAttribute("user", user);
            model.addAttribute("message", "用户信息修改失败");
            return "edit";
        }
        model.addAttribute("user", updatedUser);
        model.addAttribute("message", "用户信息修改成功");
        return "show";
    }
}
