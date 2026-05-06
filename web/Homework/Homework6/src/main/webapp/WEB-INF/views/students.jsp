<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>学生信息管理</title>
    <style>
        body {
            font-family: Arial, "Microsoft YaHei", sans-serif;
            margin: 32px;
            color: #222;
        }

        h1 {
            font-size: 24px;
            margin-bottom: 16px;
        }

        form {
            margin: 12px 0 24px;
        }

        label {
            display: inline-block;
            width: 72px;
            margin-bottom: 8px;
        }

        input {
            width: 220px;
            padding: 5px;
            margin-bottom: 8px;
        }

        button {
            padding: 6px 14px;
            cursor: pointer;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            max-width: 900px;
        }

        th, td {
            border: 1px solid #999;
            padding: 8px;
            text-align: left;
        }

        th {
            background: #f2f2f2;
        }

        .message {
            color: #0a7a28;
            margin: 12px 0;
        }
    </style>
</head>
<body>
<h1>学生保存操作</h1>

<c:if test="${not empty message}">
    <div class="message">${message}</div>
</c:if>

<form action="${pageContext.request.contextPath}/students/save" method="post">
    <div>
        <label>学号</label>
        <input type="text" name="studentNo" required>
    </div>
    <div>
        <label>姓名</label>
        <input type="text" name="name" required>
    </div>
    <div>
        <label>年龄</label>
        <input type="number" name="age" required>
    </div>
    <div>
        <label>班级</label>
        <input type="text" name="className" required>
    </div>
    <button type="submit">保存学生</button>
</form>

<h2>学生列表</h2>
<table>
    <thead>
    <tr>
        <th>ID</th>
        <th>学号</th>
        <th>姓名</th>
        <th>年龄</th>
        <th>班级</th>
        <th>操作</th>
    </tr>
    </thead>
    <tbody>
    <c:forEach items="${students}" var="item">
        <tr>
            <td>${item.id}</td>
            <td>${item.studentNo}</td>
            <td>${item.name}</td>
            <td>${item.age}</td>
            <td>${item.className}</td>
            <td>
                <form action="${pageContext.request.contextPath}/students/delete" method="post" style="display:inline;">
                    <input type="hidden" name="id" value="${item.id}">
                    <button type="submit">删除</button>
                </form>
            </td>
        </tr>
    </c:forEach>
    </tbody>
</table>

<h2>修改学生</h2>
<form action="${pageContext.request.contextPath}/students/update" method="post">
    <div>
        <label>ID</label>
        <input type="number" name="id" required>
    </div>
    <div>
        <label>姓名</label>
        <input type="text" name="name" required>
    </div>
    <div>
        <label>年龄</label>
        <input type="number" name="age" required>
    </div>
    <div>
        <label>班级</label>
        <input type="text" name="className" required>
    </div>
    <button type="submit">修改学生</button>
</form>
</body>
</html>
