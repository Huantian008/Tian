# Tian Code Playground

个人练习仓库已经重新梳理为按语言分类的结构，方便定位各类示例和后续扩展。

## 目录结构

- `java/`
  - `hello-intellij/`：IntelliJ 创建的入门项目，包含简单的 `Main` 类示例。
  - `exercise2/`：Eclipse Module `Exercise2` 的练习源码。
  - `javawork/`：多包结构的综合练习集合，涵盖类与继承等基础概念。
  - `basics-test/`：模块 `test` 下的基础语法示例和小练习。
  - `oop-practice/`：模块 `test3`，练习面向对象编程相关的类与方法。
- `cpp/`
  - `exercises/`：C++ 语法练习与算法题解合集 (`exercise*.cpp`)。
  - `book-of-cpp/`：《Book of C++》章节练习源码。
  - `oj/`：在线评测题目实现（如 `1000.cpp`–`1003.cpp`）。
- `c/`
  - `src/`：C 语言基础练习 `exciese.c`。
- `web/`
  - `frontend/`：静态网页资源（HTML/CSS/JS 和图片）。
  - `backend/`：使用 Express 的 Node.js 接口服务（`server.js` + `package.json`）。

## 使用说明

- **Java**：可直接将对应子目录导入到 IDE 中，`src` 已保留模块和包结构。编译产物与 IDE 配置已移除，可按照需要重新生成。
- **C / C++**：源代码集中在 `src` 或子目录中，可通过命令行或 IDE 编译运行，编译输出请保持在版本控制之外。
- **Web 后端**：进入 `web/backend` 后执行 `npm install` 安装依赖，使用 `npm run dev` 或 `npm start` 启动服务；静态前端位于 `web/frontend`。

## 仓库规范

- `.gitignore` 已配置忽略依赖、编译输出以及 IDE 生成文件，保持仓库整洁。
- 新增练习时建议遵循现有的语言分层目录结构，并为重要示例编写简要说明。
