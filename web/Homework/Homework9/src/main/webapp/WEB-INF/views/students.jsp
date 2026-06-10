<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>学生信息管理</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/style.css">
</head>
<body>
<div class="container">
    <div class="top-bar">
        <h2>学生信息管理</h2>
        <div>
            <a class="button" href="${pageContext.request.contextPath}/students/add">添加学生</a>
            <a class="button gray" href="${pageContext.request.contextPath}/logout">退出登录</a>
        </div>
    </div>

    <form class="inline-form" action="${pageContext.request.contextPath}/students/search" method="get">
        <input type="text" name="keyword" value="${keyword}" placeholder="输入学号或姓名查询">
        <button type="submit">查询</button>
        <a class="button gray" href="${pageContext.request.contextPath}/students">显示全部</a>
    </form>

    <table>
        <tr>
            <th>ID</th>
            <th>学号</th>
            <th>姓名</th>
            <th>性别</th>
            <th>年龄</th>
            <th>班级</th>
            <th>电话</th>
            <th>操作</th>
        </tr>
        <c:forEach items="${students}" var="student">
            <tr>
                <td>${student.id}</td>
                <td>${student.studentNo}</td>
                <td>${student.name}</td>
                <td>${student.gender}</td>
                <td>${student.age}</td>
                <td>${student.className}</td>
                <td>${student.phone}</td>
                <td class="actions">
                    <a class="button" href="${pageContext.request.contextPath}/students/edit?id=${student.id}">修改</a>
                    <a class="button red" href="${pageContext.request.contextPath}/students/delete?id=${student.id}"
                       onclick="return confirm('确定删除这条学生信息吗？')">删除</a>
                </td>
            </tr>
        </c:forEach>
        <c:if test="${empty students}">
            <tr>
                <td colspan="8">暂无学生信息</td>
            </tr>
        </c:if>
    </table>
</div>
</body>
</html>
