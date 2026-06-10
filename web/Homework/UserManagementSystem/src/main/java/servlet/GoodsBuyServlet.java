package servlet;

import model.Goods;
import model.Order;
import service.GoodsService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet(name = "GoodsBuyServlet", urlPatterns = "/goods_buy")
public class GoodsBuyServlet extends HttpServlet {
    private GoodsService gService = new GoodsService();

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doGet(request, response);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        Order order = (Order) request.getSession().getAttribute("order");
        if (order == null) {
            order = new Order();
            request.getSession().setAttribute("order", order);
        }

        int goodsid = parseInt(request.getParameter("goodsid"), parseInt(request.getParameter("id"), 0));
        String action = request.getParameter("action");
        if ("less".equals(action)) {
            order.less(goodsid);
        } else if ("delete".equals(action)) {
            order.delete(goodsid);
        } else {
            Goods goods = gService.getGoodsById(goodsid);
            if (goods != null && goods.getStock() > 0) {
                order.addGoods(goods);
                request.getSession().setAttribute("cartMsg", "已加入购物车！");
            } else {
                request.getSession().setAttribute("cartMsg", "商品不存在或库存不足！");
            }
        }
        response.sendRedirect(request.getContextPath() + "/cart.jsp");
    }

    private int parseInt(String value, int defaultValue) {
        try {
            return Integer.parseInt(value);
        } catch (Exception e) {
            return defaultValue;
        }
    }
}
