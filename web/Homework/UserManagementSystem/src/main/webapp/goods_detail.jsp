<%@ page import="model.Goods" %>
<%@ page import="model.User" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    String ctx = request.getContextPath();
    Goods goods = (Goods) request.getAttribute("goods");
    User user = (User) session.getAttribute("user");
    if (goods == null) {
        response.sendRedirect(ctx + "/index");
        return;
    }
%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title><%= goods.getName() %> - UserManagementSystem 蛋糕网上商城</title>
    <style>
        body { font-family: Arial, "Microsoft YaHei", sans-serif; margin: 0; color: #333; background: #fafafa; }
        .top { background: #8b3a2b; color: white; padding: 18px 40px; }
        .top h1 { margin: 0 0 8px; font-size: 24px; }
        .top a { color: white; margin-right: 16px; text-decoration: none; }
        .wrap { width: 980px; max-width: calc(100% - 40px); margin: 24px auto; background: white; border: 1px solid #ddd; padding: 24px; }
        .detail { display: grid; grid-template-columns: 320px 1fr; gap: 28px; }
        .placeholder { height: 190px; line-height: 190px; text-align: center; background: #f1e6df; color: #8b3a2b; margin-bottom: 12px; }
        .small { height: 90px; line-height: 90px; }
        .price { color: #c0392b; font-size: 22px; font-weight: bold; }
        .btn { display: inline-block; background: #8b3a2b; color: white; padding: 8px 18px; text-decoration: none; border: none; cursor: pointer; }
        @media (max-width: 760px) { .detail { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
<div class="top">
    <h1>UserManagementSystem 蛋糕网上商城</h1>
    <a href="<%= ctx %>/index">首页</a>
    <a href="<%= ctx %>/cart.jsp">购物车</a>
    <% if (user == null) { %>
        <a href="<%= ctx %>/user_login.jsp">登录</a>
    <% } else { %>
        <a href="<%= ctx %>/user_center.jsp">个人中心（<%= user.getUsername() %>）</a>
    <% } %>
</div>

<div class="wrap">
    <div class="detail">
        <div>
            <div class="placeholder">商品图片</div>
            <div class="placeholder small">详情图1</div>
            <div class="placeholder small">详情图2</div>
        </div>
        <div>
            <h2><%= goods.getName() %></h2>
            <p>分类：<%= goods.getType().getName() == null ? "未分类" : goods.getType().getName() %></p>
            <p class="price">￥<%= goods.getPrice() %></p>
            <p>库存：<%= goods.getStock() %></p>
            <p>商品介绍：<%= goods.getIntro() == null ? "暂无介绍。" : goods.getIntro() %></p>
            <form action="<%= ctx %>/goods_buy" method="post">
                <input type="hidden" name="goodsid" value="<%= goods.getId() %>">
                <button class="btn" type="submit">立即购买</button>
            </form>
        </div>
    </div>
</div>
</body>
</html>
