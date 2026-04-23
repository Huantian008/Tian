# C++ 学习代码

这个目录主要用来放 C++ 学习和刷题代码，按题源分组，尽量只保留源码、头文件、VS Code 配置和工具脚本。

## 目录结构

```text
cpp/
├── .vscode/          # VS Code 构建、运行、调试配置
├── book-of-cpp/      # 教材/教程示例
├── cmake/            # CMake 最小示例
├── exercises/        # 日常练习题
├── include/          # 通用头文件和模板
├── LeetCode/         # LeetCode 题解
├── oj/               # OJ 题目
├── output/           # 根目录源码的编译输出（按需生成）
├── tools/            # 清理和编码辅助脚本
├── CLEANUP_REPORT.md
├── README_ENCODING.md
└── README.md
```

说明：

- `output/` 和各题目目录下的 `output/` 都属于编译产物目录，可以清空。
- `Code Runner` 和 VS Code 任务会在当前源文件所在目录下自动创建 `output/`。
- `.exe`、编译日志、运行日志都不建议长期保留在源码旁边。

## 当前整理规则

- 保留：`.cpp`、`.h`、`.hpp`、工具脚本、VS Code 配置、说明文档
- 清理：`.exe`、编译日志、运行日志、临时输出文件
- 异常文件：类似 `nul`、单独的二进制残留，会直接移除

## 常用方式

### VS Code 任务

- `C++: Build active file`
- `C++: Run active file`
- `C++: Build and run active file`

输出位置统一为当前源码目录下的 `output/`。

### Code Runner

当前工作区已经配置好：

- `C` 使用 `tools/code-runner-c.ps1`
- `C++` 使用 `tools/code-runner-cpp.ps1`

会自动编译到当前源码目录下的 `output/`，并带时间戳命名。

### 清理临时文件

在 `E:\code\cpp` 下执行：

```bash
bash tools/clean.sh
```

## 统计

- `.cpp` 源文件：45 个
- 头文件：2 个（`.h` / `.hpp`）
- 说明文档：4 个

整体目标是让这个目录长期保持“源码和工具分开、生成物可随时清掉”的状态。
