<%@ page import="model.User" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    User user = (User) session.getAttribute("user");
    if (user == null) {
        response.sendRedirect(request.getContextPath() + "/user_login.jsp");
        return;
    }
%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>个人中心 - UserManagementSystem 蛋糕网上商城</title>
    <style>
        body { font-family: Arial, "Microsoft YaHei", sans-serif; margin: 0; background: #fafafa; color: #333; }
        .top { background: #8b3a2b; color: white; padding: 18px 40px; }
        .top h1 { margin: 0 0 8px; font-size: 24px; }
        .top a { color: white; margin-right: 16px; text-decoration: none; }
        .wrap { margin: 30px 40px; }
        label { display: inline-block; width: 90px; margin-bottom: 10px; }
        input { width: 260px; padding: 5px; }
        button { padding: 6px 18px; }
        .ok { color: green; }
        .err { color: red; }
        .box { border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; width: 430px; }
    </style>
</head>
<body>
<div class="top">
    <h1>UserManagementSystem 蛋糕网上商城</h1>
    <a href="<%= request.getContextPath() %>/index">首页</a>
    <a href="<%= request.getContextPath() %>/cart.jsp">购物车</a>
    <a href="<%= request.getContextPath() %>/user_logout">退出登录</a>
</div>
<div class="wrap">
<h2>个人中心</h2>
<p>欢迎你，<%= user.getUsername() %></p>
<p class="ok">${msg}</p>
<p class="err">${failMsg}</p>

<div class="box">
    <h3>当前用户信息</h3>
    <p>邮箱：<%= user.getEmail() %></p>
    <p>姓名：<%= user.getName() == null ? "" : user.getName() %></p>
    <p>电话：<%= user.getPhone() == null ? "" : user.getPhone() %></p>
    <p>地址：<%= user.getAddress() == null ? "" : user.getAddress() %></p>
</div>

<div class="box">
    <h3>修改收件信息</h3>
    <form action="user_changeaddress" method="post">
        <p><label>姓名：</label><input type="text" name="name" value="<%= user.getName() == null ? "" : user.getName() %>"></p>
        <p><label>电话：</label><input type="text" name="phone" value="<%= user.getPhone() == null ? "" : user.getPhone() %>"></p>
        <p><label>地址：</label><input type="text" name="address" value="<%= user.getAddress() == null ? "" : user.getAddress() %>"></p>
        <p><button type="submit">保存收件信息</button></p>
    </form>
</div>

<div class="box">
    <h3>修改密码</h3>
    <form action="user_changepwd" method="post">
        <p><label>原密码：</label><input type="password" name="password" required></p>
        <p><label>新密码：</label><input type="password" name="newPassword" required></p>
        <p><button type="submit">修改密码</button></p>
    </form>
</div>

<p><a href="user_logout">退出登录</a> <a href="<%= request.getContextPath() %>/index">返回首页</a></p>
</div>
</body>
</html>
