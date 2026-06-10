package servlet;

import model.User;
import org.apache.commons.beanutils.BeanUtils;
import service.UserService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;

@WebServlet(name = "user_changeaddress", urlPatterns = "/user_changeaddress")
public class UserChangeAddressServlet extends HttpServlet {
    private UserService uService = new UserService();

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        User loginUser = (User) request.getSession().getAttribute("user");
        if (loginUser == null) {
            response.sendRedirect(request.getContextPath() + "/user_login.jsp");
            return;
        }
        try {
            BeanUtils.copyProperties(loginUser, request.getParameterMap());
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        }
        uService.updateUserAddress(loginUser);
        User freshUser = uService.selectById(loginUser.getId());
        if (freshUser != null) {
            request.getSession().setAttribute("user", freshUser);
        }
        request.setAttribute("msg", "收件信息更新成功！");
        request.getRequestDispatcher("/user_center.jsp").forward(request, response);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        User loginUser = (User) request.getSession().getAttribute("user");
        if (loginUser != null) {
            User freshUser = uService.selectById(loginUser.getId());
            if (freshUser != null) {
                request.getSession().setAttribute("user", freshUser);
            }
        }
        request.getRequestDispatcher("/user_center.jsp").forward(request, response);
    }
}
