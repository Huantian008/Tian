<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>用户登录</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/style.css">
</head>
<body>
<h1>用户登录</h1>
<p class="nav"><a href="${pageContext.request.contextPath}/user/query">查询用户信息</a></p>
<p class="message">${message}</p>
<form action="${pageContext.request.contextPath}/user/login" method="post">
    <div>
        <label>用户名</label>
        <input type="text" name="username" value="zhangsan" required>
    </div>
    <button type="submit">登录</button>
</form>
</body>
</html>
