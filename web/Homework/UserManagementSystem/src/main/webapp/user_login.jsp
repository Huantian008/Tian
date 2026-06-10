<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>用户登录</title>
    <style>
        body { font-family: Arial, "Microsoft YaHei", sans-serif; margin: 40px; }
        label { display: inline-block; width: 100px; margin-bottom: 10px; }
        input { width: 240px; padding: 5px; }
        button { padding: 6px 18px; }
        .ok { color: green; }
        .err { color: red; }
    </style>
</head>
<body>
<h2>用户登录</h2>
<p class="ok">${msg}</p>
<p class="err">${failMsg}</p>
<form action="user_login" method="post">
    <p><label>用户名/邮箱：</label><input type="text" name="ue" required></p>
    <p><label>密码：</label><input type="password" name="password" required></p>
    <p>
        <button type="submit">登录</button>
        <button type="reset">重置</button>
    </p>
</form>
<p><a href="user_register.jsp">没有账号，去注册</a> <a href="index.jsp">返回首页</a></p>
</body>
</html>
