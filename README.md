# Tian Code Playground

个人练习仓库，按语言分目录组织，便于定位与维护。

## 目录结构

- `Java/`
  - `javawork/`：Java 主练习模块（含 `legacy/` 历史示例）
- `cpp/`
  - `exercises/`：C++ 语法练习与算法题
  - `book-of-cpp/`：书籍章节练习
  - `oj/`：在线评测题解
  - `cmake/`：CMake 示例
- `c/`
  - `src/`：C 语言基础练习
- `python/`
  - Python 学习脚本
- `web/`
  - `frontend/`：静态前端资源
  - `backend/`：Node.js/Express 示例
  - `homework/`：归并后的网页作业目录（保留原项目名：`web`、`web2`、`web3`、`web4`、`web-big homework`、`work`、`Markdown`）
- `tools/`
  - `scratch/`：临时测试目录（如 `.tmp_vsc_lang_test`）

## 使用说明

- **Java**：进入 `Java/` 后运行 `pwsh ./run_all.ps1`。
- **C / C++**：按子目录构建；构建输出目录不纳入版本控制。
- **Web 后端**：进入 `web/backend` 执行 `npm install` 与 `npm run dev`。
- **Web 作业**：进入 `web/homework` 访问各子项目目录。

## 仓库规范

- `.gitignore` 已配置忽略依赖、编译输出和 IDE 生成文件。
- 新增练习建议放到现有语言目录下，并补充简要说明。
