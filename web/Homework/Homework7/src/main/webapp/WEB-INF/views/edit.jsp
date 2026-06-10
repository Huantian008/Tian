<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>编辑用户信息</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/style.css">
</head>
<body>
<h1>编辑用户信息</h1>
<p class="message">${message}</p>
<form action="${pageContext.request.contextPath}/user/update" method="post">
    <input type="hidden" name="id" value="${user.id}">
    <div>
        <label>用户名</label>
        <input type="text" name="username" value="${user.username}" required>
    </div>
    <div>
        <label>密码</label>
        <input type="text" name="password" value="${user.password}" required>
    </div>
    <div>
        <label>姓名</label>
        <input type="text" name="realName" value="${user.realName}" required>
    </div>
    <div>
        <label>性别</label>
        <input type="text" name="gender" value="${user.gender}" required>
    </div>
    <div>
        <label>年龄</label>
        <input type="number" name="age" value="${user.age}" required>
    </div>
    <div>
        <label>电话</label>
        <input type="text" name="phone" value="${user.phone}" required>
    </div>
    <div>
        <label>邮箱</label>
        <input type="email" name="email" value="${user.email}" required>
    </div>
    <div>
        <label>地址</label>
        <input type="text" name="address" value="${user.address}" required>
    </div>
    <button type="submit">提交修改</button>
    <a class="button-link" href="${pageContext.request.contextPath}/user/query">返回查询</a>
</form>
</body>
</html>
