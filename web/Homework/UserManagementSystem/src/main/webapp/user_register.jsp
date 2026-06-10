<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>用户注册</title>
    <style>
        body { font-family: Arial, "Microsoft YaHei", sans-serif; margin: 40px; }
        label { display: inline-block; width: 80px; margin-bottom: 10px; }
        input { width: 240px; padding: 5px; }
        button { padding: 6px 18px; }
        .msg { color: red; }
    </style>
</head>
<body>
<h2>用户注册</h2>
<p class="msg">${msg}</p>
<form action="user_register" method="post">
    <p><label>用户名：</label><input type="text" name="username" required></p>
    <p><label>邮箱：</label><input type="email" name="email" required></p>
    <p><label>密码：</label><input type="password" name="password" required></p>
    <p><label>姓名：</label><input type="text" name="name"></p>
    <p><label>电话：</label><input type="text" name="phone"></p>
    <p><label>地址：</label><input type="text" name="address"></p>
    <p>
        <button type="submit">注册</button>
        <button type="reset">重置</button>
    </p>
</form>
<p><a href="user_login.jsp">已有账号，去登录</a> <a href="index.jsp">返回首页</a></p>
</body>
</html>
