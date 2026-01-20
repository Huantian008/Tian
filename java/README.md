# Java 学习代码

Java 学习和练习项目集合，包含多个独立的学习模块。

## 📁 项目结构

```
Java/
├── basics-test/      # 基础测试（10 个文件）
├── exercise2/        # 练习 2（1 个文件）
├── hello-intellij/   # IntelliJ 入门（1 个文件）
├── javawork/         # Java 练习作业（20 个文件）
├── oop-practice/     # OOP 练习（2 个文件）
├── .vscode/          # VS Code 配置
├── .idea/            # IntelliJ 配置
├── .gitignore        # Git 忽略配置
├── run_all.ps1       # 一键编译运行脚本
└── AGENTS.md         # 代理指南
```

## 🚀 快速开始

### 编译运行所有项目（推荐）
```powershell
pwsh ./run_all.ps1
```

### 编译单个项目
```bash
# 进入项目目录
cd basics-test

# 清理并编译
rm -rf out && mkdir out
javac -d out $(find src -name '*.java')

# 运行
java -cp out Mankind
```

## 📊 项目说明

### basics-test
基础测试和练习，包含：
- Mankind 继承示例
- work4 练习
- ArraySearchExample（数组搜索）
- Employee（员工类）
- FactorialSum（阶乘求和）
- HuanTian（环境测试）
- RunnoobTest（菜鸟教程测试）

### exercise2
练习题 2

### hello-intellij
IntelliJ IDEA 入门示例

### javawork
Java 练习作业，包含多个子模块：
- javawork.E
- javawork.Plant（植物类）
- javawork.work1-4（系列练习）
- javawork.StudentID（学号验证）
- javawork2.People（人类类）
- javatest.E
- pack3.c
- javawork3.E
- javawork4.Vegetable（蔬菜类）

### oop-practice
面向对象编程练习

## 🛠️ 开发工具

### 推荐使用
- **IntelliJ IDEA**：已包含 `.iml` 项目文件
- **VS Code**：已包含 `.vscode` 配置

### 编译要求
- JDK 17+（推荐 LTS 版本）
- PowerShell（用于运行 `run_all.ps1`）

## 📝 编码规范

- 4 空格缩进
- 类名使用 PascalCase
- 方法和变量使用 camelCase
- 包名全小写
- 每个文件一个 public 类

## 📖 文档

- [AGENTS.md](AGENTS.md) - 项目指南和代理说明

## 📈 统计

- Java 源文件：34 个
- 代码总行数：约 965 行
- 项目模块：5 个

---

使用 IntelliJ IDEA 或 VS Code 打开即可开始学习！
