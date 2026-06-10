import model.Goods;
import model.Order;
import model.Type;
import model.User;
import org.junit.Test;
import service.GoodsService;
import service.UserService;
import utils.PriceUtils;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.lang.reflect.Method;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

public class UserManagementAcceptanceTest {
    @Test
    public void userModelContainsFieldsRequiredByHomework() throws Exception {
        User user = new User();
        user.setUsername("testuser");
        user.setEmail("test@example.com");
        user.setPassword("123456");
        user.setName("测试用户");
        user.setPhone("13800000000");
        user.setAddress("测试地址");
        user.setIsadmin(false);
        user.setIsvalidate(false);

        assertEquals("testuser", user.getUsername());
        assertEquals("test@example.com", user.getEmail());
        assertEquals("123456", user.getPassword());
        assertEquals("测试用户", user.getName());
        assertEquals("13800000000", user.getPhone());
        assertEquals("测试地址", user.getAddress());
        assertEquals(false, user.isIsadmin());
        assertEquals(false, user.isIsvalidate());
    }

    @Test
    public void serviceExposesUserManagementMethods() throws Exception {
        Class<UserService> serviceClass = UserService.class;
        assertNotNull(serviceClass.getDeclaredMethod("register", User.class));
        assertNotNull(serviceClass.getDeclaredMethod("login", String.class, String.class));
        assertNotNull(serviceClass.getDeclaredMethod("selectById", int.class));
        assertNotNull(serviceClass.getDeclaredMethod("updateUserAddress", User.class));
        assertNotNull(serviceClass.getDeclaredMethod("updatePwd", User.class));
        assertNotNull(serviceClass.getDeclaredMethod("delete", int.class));
    }

    @Test
    public void servletRoutesMatchHomeworkDocument() throws Exception {
        assertServlet("servlet.UserRegisterServlet");
        assertServlet("servlet.UserLoginServlet");
        assertServlet("servlet.UserLogoutServlet");
        assertServlet("servlet.UserChangeAddressServlet");
        assertServlet("servlet.UserChangePwd");
    }

    @Test
    public void cakeShopModelsSupportGoodsTypeAndCartOperations() {
        Type type = new Type(1, "冰淇淋系列");
        Goods goods = new Goods();
        goods.setId(9);
        goods.setName("草莓冰淇淋");
        goods.setPrice(29.9f);
        goods.setStock(10);
        goods.setType(type);

        assertEquals("草莓冰淇淋", goods.getName());
        assertEquals("冰淇淋系列", goods.getType().getName());

        Order order = new Order();
        order.addGoods(goods);
        order.addGoods(goods);

        assertEquals(2, order.getAmount());
        assertEquals(59.8f, order.getTotal(), 0.0001f);
        assertEquals(1, order.getItemList().size());
        assertEquals(2, order.getItemMap().get(9).getAmount());

        order.less(9);
        assertEquals(1, order.getAmount());
        assertEquals(29.9f, order.getTotal(), 0.0001f);

        order.delete(9);
        assertEquals(0, order.getAmount());
        assertEquals(0.0f, order.getTotal(), 0.0001f);
        assertTrue(order.getItemList().isEmpty());
    }

    @Test
    public void cakeShopServiceAndServletRoutesMatchHomeworkDocument() throws Exception {
        Class<GoodsService> serviceClass = GoodsService.class;
        assertNotNull(serviceClass.getDeclaredMethod("getGoodsList", int.class));
        assertNotNull(serviceClass.getDeclaredMethod("getGoodsList", int.class, int.class, int.class));
        assertNotNull(serviceClass.getDeclaredMethod("getScrollGood"));
        assertNotNull(serviceClass.getDeclaredMethod("getGoodsById", int.class));
        assertNotNull(serviceClass.getDeclaredMethod("addRecommend", int.class, int.class));
        assertNotNull(serviceClass.getDeclaredMethod("removeRecommend", int.class, int.class));
        assertNotNull(serviceClass.getDeclaredMethod("insert", Goods.class));
        assertNotNull(serviceClass.getDeclaredMethod("update", Goods.class));
        assertNotNull(serviceClass.getDeclaredMethod("delete", int.class));

        assertServlet("servlet.IndexServlet");
        assertServlet("servlet.GoodsBuyServlet");
        assertServlet("servlet.GoodsDetailServlet");
    }

    @Test
    public void cakeShopJspPagesExistForHomeworkScreens() {
        assertTrue(Files.exists(Paths.get("src/main/webapp/index.jsp")));
        assertTrue(Files.exists(Paths.get("src/main/webapp/goods_detail.jsp")));
        assertTrue(Files.exists(Paths.get("src/main/webapp/cart.jsp")));
        assertTrue(Files.exists(Paths.get("src/main/webapp/user_center.jsp")));
    }

    @Test
    public void priceUtilsUsesPreciseDecimalArithmetic() {
        assertEquals(0.3f, PriceUtils.add(0.1f, 0.2f), 0.00001f);
        assertEquals(0.3d, PriceUtils.add(0.1d, 0.2d), 0.0000001d);
        assertEquals(0.1f, PriceUtils.subtract(0.3f, 0.2f), 0.00001f);
        assertEquals(0.1d, PriceUtils.subtract(0.3d, 0.2d), 0.0000001d);
    }

    private void assertServlet(String className) throws Exception {
        Class<?> servletClass = Class.forName(className);
        Method doPost = servletClass.getDeclaredMethod("doPost",
                javax.servlet.http.HttpServletRequest.class,
                javax.servlet.http.HttpServletResponse.class);
        assertNotNull(doPost);
    }
}
