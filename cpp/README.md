# C++ 学习代码

简洁的 C++ 代码仓库，已统一 UTF-8 编码，解决中文乱码问题。

## 📁 目录结构

```
cpp/
├── LeetCode/          # LeetCode 题解（3 个）
├── book-of-cpp/       # 教程示例（6 个）
├── exercises/         # 练习题（25 个）
├── oj/               # 在线评测（3 个）
├── include/          # 头文件和模板
│   ├── utf8_console.hpp      # UTF-8 支持
│   ├── cpp_template.cpp      # 代码模板
│   └── README_中文输出指南.md
├── tools/            # 工具脚本
│   ├── fix_encoding.py       # 编码修复
│   └── clean.sh              # 清理工具
├── .vscode/          # VS Code 配置
└── 文档
    ├── README.md              # 本文档
    ├── README_ENCODING.md    # 编码详细说明
    └── CLEANUP_REPORT.md      # 清理报告
```

## ✨ 特性

- ✅ 所有文件统一 UTF-8 编码
- ✅ 换行符统一为 LF
- ✅ 包含中文的程序已添加编译器指令
- ✅ 移除平台特定代码，跨平台兼容

## 🚀 快速开始

### 编译运行
```bash
g++ your_file.cpp -o output
./output
```

### 中文输出（Windows）
包含头文件并在 main 函数开头调用：
```cpp
#include "include/utf8_console.hpp"

int main() {
    init_utf8_console();
    std::cout << "你好，世界！" << std::endl;
    return 0;
}
```

## 🛠️ 工具

### 修复编码
```bash
python3 tools/fix_encoding.py
```

### 清理临时文件
```bash
bash tools/clean.sh
```

## 📖 文档

- [README_ENCODING.md](README_ENCODING.md) - 编码详细说明和常见问题
- [CLEANUP_REPORT.md](CLEANUP_REPORT.md) - 文件夹清理报告
- [include/README_中文输出指南.md](include/README_中文输出指南.md) - 中文输出详细指南

## 📊 统计

- 源文件：43 个
- 头文件：1 个
- 总文件数：46 个

---

使用 VS Code 打开，配置已包含 UTF-8 支持！
