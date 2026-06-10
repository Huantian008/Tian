<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>修改学生</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/style.css">
</head>
<body>
<div class="container">
    <h2>修改学生</h2>
    <form action="${pageContext.request.contextPath}/students/edit" method="post">
        <input type="hidden" name="id" value="${student.id}">

        <label>学号</label>
        <input type="text" name="studentNo" value="${student.studentNo}" required>

        <label>姓名</label>
        <input type="text" name="name" value="${student.name}" required>

        <label>性别</label>
        <select name="gender">
            <option value="男" ${student.gender == '男' ? 'selected' : ''}>男</option>
            <option value="女" ${student.gender == '女' ? 'selected' : ''}>女</option>
        </select>

        <label>年龄</label>
        <input type="number" name="age" value="${student.age}" min="1" required>

        <label>班级</label>
        <input type="text" name="className" value="${student.className}" required>

        <label>电话</label>
        <input type="text" name="phone" value="${student.phone}">

        <div class="form-actions">
            <button type="submit">保存修改</button>
            <a class="button gray" href="${pageContext.request.contextPath}/students">返回</a>
        </div>
    </form>
</div>
</body>
</html>
