# Java 学习代码

Java 练习已收敛为单一主模块 `javawork`，历史练习迁移到 `legacy` 包下统一维护。

## 📁 项目结构

```
Java/
├── javawork/
│   ├── src/
│   │   ├── javawork*/        # 现有练习包
│   │   └── legacy/           # 迁移自旧模块的历史练习
│   └── out/                  # 编译输出（可清理）
├── .vscode/
├── .idea/
├── .gitignore
├── run_all.ps1
├── compile.sh
├── clean.sh
├── clean.bat
└── AGENTS.md
```

## 🚀 快速开始

### 编译并运行（推荐）
```powershell
pwsh ./run_all.ps1
```

### 仅编译
```bash
./compile.sh javawork
# 或
./compile.sh all
```

### 清理产物
```bash
./clean.sh
```

```bat
clean.bat
```

## 🧩 迁移说明

- 原 `basics-test`、`hello-intellij`、`oop-practice` 示例已迁移到 `javawork/src/legacy/...`。
- `exercise2` 仅包含空模块定义，已并入整理流程后移除。
- 运行入口已在 `run_all.ps1` 中统一维护。
