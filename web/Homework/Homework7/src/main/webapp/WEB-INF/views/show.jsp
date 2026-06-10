<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>显示用户信息</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/style.css">
</head>
<body>
<h1>显示用户信息</h1>
<p class="message">${message}</p>
<table>
    <tr><th>ID</th><td>${user.id}</td></tr>
    <tr><th>用户名</th><td>${user.username}</td></tr>
    <tr><th>密码</th><td>${user.password}</td></tr>
    <tr><th>姓名</th><td>${user.realName}</td></tr>
    <tr><th>性别</th><td>${user.gender}</td></tr>
    <tr><th>年龄</th><td>${user.age}</td></tr>
    <tr><th>电话</th><td>${user.phone}</td></tr>
    <tr><th>邮箱</th><td>${user.email}</td></tr>
    <tr><th>地址</th><td>${user.address}</td></tr>
</table>
<p class="nav">
    <a href="${pageContext.request.contextPath}/user/query">继续查询</a>
    <a href="${pageContext.request.contextPath}/user/login">返回登录</a>
</p>
</body>
</html>
