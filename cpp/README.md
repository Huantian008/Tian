# C++ 学习代码仓库

个人 C++ 学习代码集中管理，涵盖教材示例、基础练习、OJ 题目和 LeetCode 刷题记录。所有代码使用 **C++17**，编译器为 MinGW GCC。

## 目录结构

```text
cpp/
├── book-of-cpp/     # 教材/教程示例代码（按章节编号）
├── exercises/       # 基础练习题（26 道，递进式）
├── LeetCode/        # LeetCode 题解（3 题）
├── oj/              # OJ 平台题目（5 题）
├── .vscode/         # VS Code 构建/调试/运行配置
└── output/          # 根目录编译产物
```

各子目录内均有 `output/` 文件夹存放编译生成的 `.exe` 文件，可随时清空重建。

## 内容概览

### book-of-cpp/ — 教材示例
| 文件 | 内容 |
|---|---|
| 3.1.1.cpp | `sizeof` 基础类型大小 |
| 3.1.8.cpp | ASCII 字符输出 |
| 3.1.10.cpp | 布尔类型输出 |
| 3.3.1.cpp | `if` 条件判断与逻辑运算符 |
| 4.3.7.cpp | 嵌套循环：九九乘法表 |
| 5.1.1.cpp | `std::vector` 基本操作 |

### exercises/ — 基础练习
涵盖输入输出、循环、数组、指针与引用、动态内存、`std::vector`、`std::stack`、字符串处理、随机数、递归（汉诺塔）、可变参数、Kadane 算法等。共 26 道题，从基础语法到算法入门递进。

### LeetCode/ — 算法练习
| 文件 | 题目 | 解法 |
|---|---|---|
| 1-twosum.cpp | #1 Two Sum | 暴力双重循环 |
| 1-2twosum.cpp | #1 Two Sum | 哈希表优化 O(n) |
| 9-1.cpp | #9 Palindrome Number | 字符串双指针 |

### oj/ — OJ 平台题目
| 文件 | 题目 |
|---|---|
| 1000.cpp | A+B 基础输入输出 |
| 1001.cpp / 1001.1.cpp | 累加求和 |
| 1002.cpp | 大整数加法（字符串逐位计算） |
| 1003.cpp | 最大子数组和（Kadane 变体） |

## 编译与运行

### VS Code（推荐）

工作区已配置好任务和调试配置：
- **编译**: `Terminal` → `Run Build Task`（`g++.exe 生成活动文件`）
- **调试**: `F5` → 选择 `C++: Debug active file (Windows)`
- **运行**: `Ctrl+F5` → 选择 `C++: Run active file (Windows)`

编译产物自动生成到源文件所在目录的 `output/` 下。

### 手动编译

```powershell
E:\MinGW\ucrt64\bin\g++.exe -g -std=c++17 .\xxx.cpp -o .\output\xxx.exe
```

## 维护约定

- 源码按用途分类存放，新文件优先放入已有分类目录
- 编译产物统一进各目录下的 `output/`，不纳入版本管理
- 保持单文件练习为主，不引入额外依赖
