# 用户管理系统

本项目按“个人任务3：用户管理系统”完成，使用 Servlet、JSP、JDBC、Druid 和 DbUtils 实现用户注册、登录、退出、修改收件信息和修改密码。

## 数据库

先执行：

```powershell
& 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe' -uroot -pywt123YWT < schema.sql
```

数据库配置在：

```text
src/main/resources/druid.properties
```

默认连接 `cookieshop` 数据库，账号 `root`，密码 `ywt123YWT`。

## 构建

```powershell
& 'C:\Program Files\JetBrains\IntelliJ IDEA 2026.1.1\plugins\maven\lib\maven3\bin\mvn.cmd' -s maven-settings.xml clean package
```

## 运行

```powershell
.\run-tomcat9.ps1
```

访问：

```text
http://localhost:8080/UserManagementSystem/
```

示例账号：

```text
testuser / 123456
test@example.com / 123456
```
