package servlet;

import service.GoodsService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet(name = "IndexServlet", urlPatterns = "/index")
public class IndexServlet extends HttpServlet {
    private GoodsService gService = new GoodsService();

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doGet(request, response);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setAttribute("scrollGood", gService.getScrollGood());
        request.setAttribute("scrollList", gService.getGoodsList(1));
        request.setAttribute("hotList", gService.getGoodsList(2));
        request.setAttribute("newList", gService.getGoodsList(3));
        request.setAttribute("goodsList", gService.getGoodsList(0, 1, 12));
        request.getRequestDispatcher("/index.jsp").forward(request, response);
    }
}
