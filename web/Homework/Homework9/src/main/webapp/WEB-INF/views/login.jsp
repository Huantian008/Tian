<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>学生信息管理系统登录</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/style.css">
</head>
<body>
<div class="login-box">
    <h2>学生信息管理系统</h2>
    <form action="${pageContext.request.contextPath}/login" method="post">
        <label>用户名</label>
        <input type="text" name="username" required>

        <label>密码</label>
        <input type="password" name="password" required>

        <p class="message">${message}</p>
        <button type="submit">登录</button>
    </form>
    <p>默认账号：admin / 123456</p>
</div>
</body>
</html>
