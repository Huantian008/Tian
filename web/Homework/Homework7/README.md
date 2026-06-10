# 实验3 SpringMVC框架数据绑定实验

## 项目说明

本项目是一个传统 Spring MVC + JSP + MySQL 示例，完成用户信息的数据绑定实验。程序包含控制层、业务层、数据层，并通过 JSP 表单把查询到的用户信息绑定到编辑页面，提交修改后转发到显示页面。

## 环境

- JDK 8 编译目标
- Spring MVC 5.3.x
- Tomcat 9
- MySQL 8
- Maven

本项目使用 `javax.servlet`，请部署到 Tomcat 9，不要部署到 Tomcat 10。

## 数据库

配置文件：

```text
src/main/resources/jdbc.properties
```

默认配置：

```properties
jdbc.url=jdbc:mysql://localhost:3306/homework7?useSSL=false&serverTimezone=Asia/Shanghai&characterEncoding=utf8
jdbc.username=root
jdbc.password=ywt123YWT
```

建库建表：

```powershell
cmd /c "`"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe`" --default-character-set=utf8mb4 -uroot -pywt123YWT < schema.sql"
```

如果 MySQL 8.4 路径不存在，可改用：

```powershell
cmd /c "`"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe`" --default-character-set=utf8mb4 -uroot -pywt123YWT < schema.sql"
```

## 运行

在项目目录执行：

```powershell
.\run-tomcat9.ps1
```

脚本会自动执行 Maven 打包，把 `target\Homework7.war` 部署到本机已有的 Tomcat 9：

```text
E:\code\web\Homework\Homework6\tools\apache-tomcat-9.0.117
```

启动成功后访问：

```text
http://localhost:8080/Homework7/user/query
```

也可以访问登录演示：

```text
http://localhost:8080/Homework7/user/login
```

## 实验功能

- 登录用户：输入 `zhangsan`，转发到显示页面并显示“欢迎张三”。
- 查询用户：输入 `zhangsan`，查询 MySQL 后跳转到编辑页面。
- 编辑用户：修改电话、邮箱或地址，提交后转发到显示页面。
- 异常提示：查询不存在的用户名会停留在查询页面并显示提示。

## 项目结构

```text
src/main/java/com/example/homework7/controller/UserController.java
src/main/java/com/example/homework7/service/UserService.java
src/main/java/com/example/homework7/service/UserServiceImpl.java
src/main/java/com/example/homework7/dao/UserDao.java
src/main/java/com/example/homework7/dao/UserDaoImpl.java
src/main/java/com/example/homework7/model/User.java
src/main/resources/spring-mvc.xml
src/main/resources/jdbc.properties
src/main/webapp/WEB-INF/web.xml
src/main/webapp/WEB-INF/views/login.jsp
src/main/webapp/WEB-INF/views/query.jsp
src/main/webapp/WEB-INF/views/edit.jsp
src/main/webapp/WEB-INF/views/show.jsp
```
