# Java Cleanup Notes

Last updated: 2026-03-05

## 变更摘要

- Java 目录收敛为单一主模块：`javawork`
- 旧模块源码迁移到 `javawork/src/legacy/...` 后删除：
  - `basics-test`
  - `exercise2`
  - `hello-intellij`
  - `oop-practice`
- 统一脚本入口：`run_all.ps1` / `compile.sh`
- 清理脚本增强：新增 `out_tmp` 清理

## 验证命令

```powershell
pwsh ./run_all.ps1
```

```bash
./compile.sh all
./clean.sh
```
