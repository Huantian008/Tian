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
            margin: 28px;
            color: #222;
        }

        h1 {
            font-size: 24px;
            margin-bottom: 16px;
        }

        h2 {
            font-size: 18px;
            margin-top: 28px;
        }

        form {
            margin: 10px 0 18px;
        }

        label {
            display: inline-block;
            width: 64px;
            margin-bottom: 8px;
        }

        input, select {
            width: 190px;
            padding: 5px;
            margin-right: 10px;
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
            margin-top: 10px;
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
            margin: 10px 0;
        }

        .inline-form {
            display: inline;
        }
    </style>
</head>
<body>
<h1>学生信息管理</h1>

<c:if test="${not empty message}">
    <div class="message">${message}</div>
</c:if>

<h2>查询学生</h2>
<form action="${pageContext.request.contextPath}/students/search" method="get">
    <select name="searchType">
        <option value="all" ${searchType == 'all' ? 'selected' : ''}>显示全部</option>
        <option value="id" ${searchType == 'id' ? 'selected' : ''}>按ID查询</option>
        <option value="name" ${searchType == 'name' ? 'selected' : ''}>姓名模糊查询</option>
        <option value="nameAddress" ${searchType == 'nameAddress' ? 'selected' : ''}>姓名和住址组合查询</option>
    </select>
    <input type="number" name="id" placeholder="学生ID" value="${queryId}">
    <input type="text" name="name" placeholder="姓名" value="${queryName}">
    <input type="text" name="address" placeholder="住址" value="${queryAddress}">
    <button type="submit">查询</button>
    <a href="${pageContext.request.contextPath}/students">返回全部</a>
</form>

<h2>添加学生</h2>
<form action="${pageContext.request.contextPath}/students/add" method="post">
    <label>姓名</label>
    <input type="text" name="name" required>
    <label>年龄</label>
    <input type="number" name="age" required>
    <label>性别</label>
    <input type="text" name="sex" required>
    <label>住址</label>
    <input type="text" name="address" required>
    <button type="submit">添加</button>
</form>

<h2>学生列表</h2>
<table>
    <thead>
    <tr>
        <th>ID</th>
        <th>姓名</th>
        <th>年龄</th>
        <th>性别</th>
        <th>住址</th>
        <th>操作</th>
    </tr>
    </thead>
    <tbody>
    <c:forEach items="${students}" var="item">
        <tr>
            <td>${item.id}</td>
            <td>${item.name}</td>
            <td>${item.age}</td>
            <td>${item.sex}</td>
            <td>${item.address}</td>
            <td>
                <form action="${pageContext.request.contextPath}/students/delete" method="post" class="inline-form">
                    <input type="hidden" name="id" value="${item.id}">
                    <button type="submit">删除</button>
                </form>
            </td>
        </tr>
    </c:forEach>
    <c:if test="${empty students}">
        <tr>
            <td colspan="6">没有查询到学生数据</td>
        </tr>
    </c:if>
    </tbody>
</table>

<h2>修改学生</h2>
<form action="${pageContext.request.contextPath}/students/update" method="post">
    <label>ID</label>
    <input type="number" name="id" required>
    <label>姓名</label>
    <input type="text" name="name" required>
    <label>年龄</label>
    <input type="number" name="age" required>
    <label>性别</label>
    <input type="text" name="sex" required>
    <label>住址</label>
    <input type="text" name="address" required>
    <button type="submit">修改</button>
</form>
</body>
</html>
