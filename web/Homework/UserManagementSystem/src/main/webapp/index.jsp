<%@ page import="java.util.List" %>
<%@ page import="model.Goods" %>
<%@ page import="model.User" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    if (request.getAttribute("goodsList") == null) {
        request.getRequestDispatcher("/index").forward(request, response);
        return;
    }
    String ctx = request.getContextPath();
    User user = (User) session.getAttribute("user");
    Goods scrollGood = (Goods) request.getAttribute("scrollGood");
    List<Goods> scrollList = (List<Goods>) request.getAttribute("scrollList");
    List<Goods> hotList = (List<Goods>) request.getAttribute("hotList");
    List<Goods> newList = (List<Goods>) request.getAttribute("newList");
    List<Goods> goodsList = (List<Goods>) request.getAttribute("goodsList");
%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>UserManagementSystem 蛋糕网上商城</title>
    <style>
        body { font-family: Arial, "Microsoft YaHei", sans-serif; margin: 0; color: #333; background: #fafafa; }
        .top { background: #8b3a2b; color: white; padding: 18px 40px; }
        .top h1 { margin: 0 0 8px; font-size: 24px; }
        .top a { color: white; margin-right: 16px; text-decoration: none; }
        .wrap { width: 1080px; max-width: calc(100% - 40px); margin: 24px auto; }
        .hero { background: white; border: 1px solid #ddd; padding: 24px; margin-bottom: 22px; }
        .hero h2 { margin-top: 0; }
        .section { margin-bottom: 28px; }
        .section h2 { font-size: 20px; border-bottom: 2px solid #8b3a2b; padding-bottom: 8px; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
        .card { background: white; border: 1px solid #ddd; padding: 14px; }
        .placeholder { height: 90px; line-height: 90px; text-align: center; background: #f1e6df; color: #8b3a2b; margin-bottom: 10px; }
        .name { font-weight: bold; margin-bottom: 6px; }
        .price { color: #c0392b; font-weight: bold; }
        .intro { color: #666; min-height: 38px; }
        .btn { display: inline-block; background: #8b3a2b; color: white; padding: 7px 14px; text-decoration: none; margin-top: 8px; border: none; cursor: pointer; }
        .empty { color: #888; background: white; border: 1px solid #ddd; padding: 14px; }
        @media (max-width: 800px) { .grid { grid-template-columns: repeat(2, 1fr); } }
    </style>
</head>
<body>
<div class="top">
    <h1>UserManagementSystem 蛋糕网上商城</h1>
    <div>
        <a href="<%= ctx %>/index">首页</a>
        <a href="<%= ctx %>/cart.jsp">购物车</a>
        <% if (user == null) { %>
            <a href="<%= ctx %>/user_login.jsp">登录</a>
            <a href="<%= ctx %>/user_register.jsp">注册</a>
        <% } else { %>
            <a href="<%= ctx %>/user_center.jsp">个人中心（<%= user.getUsername() %>）</a>
            <a href="<%= ctx %>/user_logout">退出</a>
        <% } %>
    </div>
</div>

<div class="wrap">
    <div class="hero">
        <h2>今日推荐</h2>
        <% if (scrollGood != null) { %>
            <div class="placeholder">商品图片</div>
            <h3><%= scrollGood.getName() %></h3>
            <p><%= scrollGood.getIntro() == null ? "新鲜蛋糕，欢迎选购。" : scrollGood.getIntro() %></p>
            <p class="price">￥<%= scrollGood.getPrice() %></p>
            <a class="btn" href="<%= ctx %>/goods_detail?id=<%= scrollGood.getId() %>">查看详情</a>
        <% } else { %>
            <p>暂无推荐商品。</p>
        <% } %>
    </div>

    <div class="section">
        <h2>轮播推荐</h2>
        <div class="grid">
            <% if (scrollList == null || scrollList.isEmpty()) { %>
                <div class="empty">暂无商品。</div>
            <% } else { for (Goods goods : scrollList) { %>
                <div class="card">
                    <div class="placeholder">商品图片</div>
                    <div class="name"><%= goods.getName() %></div>
                    <div class="intro"><%= goods.getIntro() == null ? "" : goods.getIntro() %></div>
                    <div class="price">￥<%= goods.getPrice() %></div>
                    <a class="btn" href="<%= ctx %>/goods_detail?id=<%= goods.getId() %>">详情</a>
                </div>
            <% } } %>
        </div>
    </div>

    <div class="section">
        <h2>热销商品</h2>
        <div class="grid">
            <% if (hotList == null || hotList.isEmpty()) { %>
                <div class="empty">暂无商品。</div>
            <% } else { for (Goods goods : hotList) { %>
                <div class="card">
                    <div class="placeholder">商品图片</div>
                    <div class="name"><%= goods.getName() %></div>
                    <div class="intro"><%= goods.getIntro() == null ? "" : goods.getIntro() %></div>
                    <div class="price">￥<%= goods.getPrice() %></div>
                    <a class="btn" href="<%= ctx %>/goods_detail?id=<%= goods.getId() %>">详情</a>
                </div>
            <% } } %>
        </div>
    </div>

    <div class="section">
        <h2>新品上市</h2>
        <div class="grid">
            <% if (newList == null || newList.isEmpty()) { %>
                <div class="empty">暂无商品。</div>
            <% } else { for (Goods goods : newList) { %>
                <div class="card">
                    <div class="placeholder">商品图片</div>
                    <div class="name"><%= goods.getName() %></div>
                    <div class="intro"><%= goods.getIntro() == null ? "" : goods.getIntro() %></div>
                    <div class="price">￥<%= goods.getPrice() %></div>
                    <a class="btn" href="<%= ctx %>/goods_detail?id=<%= goods.getId() %>">详情</a>
                </div>
            <% } } %>
        </div>
    </div>

    <div class="section">
        <h2>全部商品</h2>
        <div class="grid">
            <% if (goodsList == null || goodsList.isEmpty()) { %>
                <div class="empty">暂无商品。</div>
            <% } else { for (Goods goods : goodsList) { %>
                <div class="card">
                    <div class="placeholder">商品图片</div>
                    <div class="name"><%= goods.getName() %></div>
                    <div>分类：<%= goods.getType().getName() == null ? "未分类" : goods.getType().getName() %></div>
                    <div class="price">￥<%= goods.getPrice() %></div>
                    <a class="btn" href="<%= ctx %>/goods_detail?id=<%= goods.getId() %>">查看详情</a>
                </div>
            <% } } %>
        </div>
    </div>
</div>
</body>
</html>
