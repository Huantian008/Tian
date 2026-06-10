<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>添加学生</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/style.css">
</head>
<body>
<div class="container">
    <h2>添加学生</h2>
    <form action="${pageContext.request.contextPath}/students/add" method="post">
        <label>学号</label>
        <input type="text" name="studentNo" required>

        <label>姓名</label>
        <input type="text" name="name" required>

        <label>性别</label>
        <select name="gender">
            <option value="男">男</option>
            <option value="女">女</option>
        </select>

        <label>年龄</label>
        <input type="number" name="age" min="1" required>

        <label>班级</label>
        <input type="text" name="className" required>

        <label>电话</label>
        <input type="text" name="phone">

        <div class="form-actions">
            <button type="submit">保存</button>
            <a class="button gray" href="${pageContext.request.contextPath}/students">返回</a>
        </div>
    </form>
</div>
</body>
</html>
