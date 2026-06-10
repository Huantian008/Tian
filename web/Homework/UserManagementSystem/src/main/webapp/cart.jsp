<%@ page import="model.Order" %>
<%@ page import="model.OrderItem" %>
<%@ page import="model.User" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    String ctx = request.getContextPath();
    User user = (User) session.getAttribute("user");
    Order order = (Order) session.getAttribute("order");
    String cartMsg = (String) session.getAttribute("cartMsg");
    if (cartMsg != null) {
        session.removeAttribute("cartMsg");
    }
%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>购物车 - UserManagementSystem 蛋糕网上商城</title>
    <style>
        body { font-family: Arial, "Microsoft YaHei", sans-serif; margin: 0; color: #333; background: #fafafa; }
        .top { background: #8b3a2b; color: white; padding: 18px 40px; }
        .top h1 { margin: 0 0 8px; font-size: 24px; }
        .top a { color: white; margin-right: 16px; text-decoration: none; }
        .wrap { width: 980px; max-width: calc(100% - 40px); margin: 24px auto; background: white; border: 1px solid #ddd; padding: 24px; }
        table { width: 100%; border-collapse: collapse; margin-top: 16px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background: #f1e6df; }
        .btn { display: inline-block; background: #8b3a2b; color: white; padding: 6px 12px; text-decoration: none; border: none; cursor: pointer; }
        .linkbtn { background: none; border: none; color: #8b3a2b; cursor: pointer; padding: 0 8px; }
        .msg { color: green; }
        .total { text-align: right; font-weight: bold; margin-top: 16px; }
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
    <h2>购物车</h2>
    <% if (cartMsg != null) { %>
        <p class="msg"><%= cartMsg %></p>
    <% } %>
    <% if (order == null || order.getItemList().isEmpty()) { %>
        <p>购物车为空，请先去首页选择商品。</p>
        <p><a class="btn" href="<%= ctx %>/index">返回首页</a></p>
    <% } else { %>
        <table>
            <tr>
                <th>商品</th>
                <th>单价</th>
                <th>数量</th>
                <th>小计</th>
                <th>操作</th>
            </tr>
            <% for (OrderItem item : order.getItemList()) { %>
                <tr>
                    <td><%= item.getGoodsName() %></td>
                    <td>￥<%= item.getPrice() %></td>
                    <td><%= item.getAmount() %></td>
                    <td>￥<%= item.getPrice() * item.getAmount() %></td>
                    <td>
                        <form action="<%= ctx %>/goods_buy" method="post" style="display:inline;">
                            <input type="hidden" name="goodsid" value="<%= item.getGoods().getId() %>">
                            <input type="hidden" name="action" value="less">
                            <button class="linkbtn" type="submit">减少</button>
                        </form>
                        <form action="<%= ctx %>/goods_buy" method="post" style="display:inline;">
                            <input type="hidden" name="goodsid" value="<%= item.getGoods().getId() %>">
                            <input type="hidden" name="action" value="delete">
                            <button class="linkbtn" type="submit">删除</button>
                        </form>
                    </td>
                </tr>
            <% } %>
        </table>
        <p class="total">共 <%= order.getAmount() %> 件商品，合计：￥<%= order.getTotal() %></p>
        <p><a class="btn" href="<%= ctx %>/index">继续购物</a></p>
    <% } %>
</div>
</body>
</html>
