# 学生管理系统

作品信息：`11+杨文天+202599770425`

## 技术栈

- 后端：Spring Boot 3、Java 21、MyBatis、MySQL
- 前端：Vue 3、Vite、Element Plus、Axios
- 数据库：MySQL，库名 `student_management_system`

## 运行步骤

1. 导入数据库脚本：`database/student_management.sql`

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -uroot -pywt123YWT --default-character-set=utf8mb4 -e "source E:/code/web/Homework/StudentManagementSystem/database/student_management.sql"
```
2. 启动后端：

```powershell
cd backend
.\mvnw.cmd spring-boot:run
```

3. 启动前端：

```powershell
cd frontend
npm install
npm run dev
```

4. 浏览器访问前端地址，默认账号：

```text
用户名：admin
密码：123456
```

## 交付物

- 后端源码：`backend/`
- 前端源码：`frontend/`
- 数据库脚本：`database/student_management.sql`
- 作品报告：`deliverables/11+杨文天+202599770425.docx`

## 本机验证记录

- MySQL 服务：`MySQL80`，状态 Running
- MySQL 版本：8.0.45
- 数据库导入后数据量：管理员 1 条、学生 5 条、课程 4 条、成绩 8 条
- 后端真实连接 MySQL 后验证：登录成功、首页统计返回学生 5 人、课程 4 门、成绩记录 8 条
