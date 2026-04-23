# Java 学习代码

当前工作区已收口为单一主模块 `javawork`。历史练习源码统一迁移到 `javawork/src/legacy/...` 下维护，顶层只保留必要配置和说明文件。

## 项目结构

```text
Java/
├── javawork/
│   ├── src/
│   │   ├── javawork*/        # 当前练习包
│   │   └── legacy/           # 迁移自旧模块的历史练习
│   └── javawork.iml
├── .vscode/
├── .idea/
├── .gitignore
└── AGENTS.md
```

## 迁移说明

- 原 `basics-test`、`hello-intellij`、`oop-practice` 示例已迁移到 `javawork/src/legacy/...`。
- `exercise2` 仅包含空模块定义，整理时已移除。
- 顶层旧脚本和历史残留目录已删除，后续直接在 `javawork` 下手动编译、运行和清理。

## 手动使用

### 编译

在 `javawork` 目录下执行：

```powershell
Remove-Item -Recurse -Force out -ErrorAction SilentlyContinue
$sources = Get-ChildItem -Recurse -Filter *.java | ForEach-Object { $_.FullName }
javac -d out $sources
```

### 运行

编译完成后，用下面的格式运行主类：

```powershell
java -cp out <主类全限定名>
```

示例：

```powershell
java -cp out javawork.E
java -cp out legacy.hello.Main
```

### 清理产物

在 `javawork` 目录下删除编译输出目录：

```powershell
Remove-Item -Recurse -Force out -ErrorAction SilentlyContinue
```

如果工作区里以后再次出现其他编译产物，也可以一并删除 `out_tmp/`、`bin/` 和零散 `.class` 文件。
