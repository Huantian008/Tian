# 实验5 SSM框架整合实验

## 项目说明

本项目是一个简单的学生信息管理系统，使用 Spring、Spring MVC、MyBatis、JSP 和 MySQL 完成 SSM 框架整合。用户登录后可以通过 Web 页面添加、删除、修改和查询学生信息。

## 环境要求

- JDK 8 或更高版本
- Maven
- Tomcat 9
- MySQL

本项目使用 `javax.servlet` 和 Spring Framework 5.3.x，适合部署到 Tomcat 9。

## 数据库配置

数据库连接配置文件：

```text
src/main/resources/jdbc.properties
```

默认配置：

```properties
jdbc.url=jdbc:mysql://localhost:3306/homework9?useSSL=false&serverTimezone=Asia/Shanghai&characterEncoding=utf8
jdbc.username=root
jdbc.password=ywt123YWT
```

运行前先在 MySQL 中执行：

```sql
source E:/code/web/Homework/Homework9/schema.sql;
```

默认登录账号：

```text
admin / 123456
```

## 打包运行

在项目目录执行：

```powershell
mvn -s maven-settings.xml clean package
```

如果命令行没有配置 Maven，可以使用 IDEA 自带 Maven：

```powershell
& "C:\Program Files\JetBrains\IntelliJ IDEA 2026.1.1\plugins\maven\lib\maven3\bin\mvn.cmd" -s maven-settings.xml clean package
```

将生成的 WAR 部署到 Tomcat 9：

```text
target/Homework9.war -> Tomcat9/webapps/Homework9.war
```

启动 Tomcat 后访问：

```text
http://localhost:8080/Homework9/login
```

## 实验小结

通过本次实验，完成了 Spring、Spring MVC 和 MyBatis 的整合配置，理解了 `applicationContext.xml`、`spring-mvc.xml`、`mybatis-config.xml` 和 `web.xml` 在项目中的作用。项目采用 Controller、Service、Mapper、Model 分层结构，使用 Spring MVC 接收请求并返回 JSP 页面，通过 MyBatis 操作 MySQL 数据库，实现了登录以及学生信息的增删改查功能。
