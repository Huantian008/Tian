# 实验2 Spring框架中Bean的管理

## 项目说明

本项目按 JDK8、Tomcat9、MySQL 环境完成 Spring Bean 管理实验。程序采用 Spring 注解装配方式，实现 `StudentController`、`StudentService`、`StudentDao` 三层调用，并通过 `JdbcTemplate` 将学生信息保存到 MySQL。

## 环境要求

- JDK 8
- Maven
- Tomcat 9
- MySQL

当前代码使用 `javax.servlet` 和 Spring Framework 5.3.x，适合部署到 Tomcat 9；不要部署到 Tomcat 10，因为 Tomcat 10 使用 `jakarta.servlet`。

## 数据库配置

数据库配置文件：

```text
src/main/resources/jdbc.properties
```

默认配置：

```properties
jdbc.driver=com.mysql.cj.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/homework6?useSSL=false&serverTimezone=Asia/Shanghai&characterEncoding=utf8
jdbc.username=root
jdbc.password=ywt123YWT
```

先在 MySQL 中执行：

```sql
source E:/code/web/Homework/Homework6/schema.sql;
```

也可以手动复制 `schema.sql` 中的建库建表语句执行。

## 运行步骤

1. 在项目目录执行打包：

```powershell
mvn clean package
```

如果 Maven Central 下载依赖失败，可以使用项目中的镜像配置：

```powershell
mvn -s maven-settings.xml clean package
```

本项目已经提供 `.mvn/maven.config`，正常情况下 IDEA Maven 同步和命令行 Maven 会自动使用 `maven-settings.xml` 中的镜像。

在本机 IDEA 里也可以直接运行：

```powershell
.\run-tomcat9.ps1
```

该脚本会自动打包、部署到项目内的 Tomcat 9，并启动访问地址。

2. 将生成的文件复制到 Tomcat 9：

```text
target/Homework6.war -> Tomcat9/webapps/Homework6.war
```

3. 启动 Tomcat 9 后访问：

```text
http://localhost:8080/Homework6/students
```

## 实验结果

页面包含：

- 学生保存表单
- 学生列表
- 删除学生功能
- 修改学生功能

运行后可以看到控制层调用业务层，业务层调用数据层，数据层通过 `JdbcTemplate` 操作 MySQL 的 `student` 表，说明 Spring IoC 和依赖注入配置成功。

## 实验小结

通过本次实验，掌握了 Spring 中 Bean 的创建和注解配置方法，理解了 `@Controller`、`@Service`、`@Repository` 等注解在三层结构中的作用。程序通过构造器注入实现了控制层、业务层和数据层之间的松耦合，使用 `JdbcTemplate` 完成了学生信息的保存、查询、修改和删除操作，加深了对 Spring 控制反转和依赖注入机制的理解。
