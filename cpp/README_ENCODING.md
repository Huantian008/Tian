# C++ 代码编码修复说明

## 修复内容

已对 `cpp/` 目录下的所有 C/C++ 源文件进行了编码统一处理，解决中文乱码问题。

## 具体修改

### 1. 文件编码统一
- 所有文件统一转换为 **UTF-8** 编码
- 换行符统一为 **LF** (Unix 格式)

### 2. 中文乱码解决
对于包含中文字符串的文件，添加了 MSVC 编译器指令：
```cpp
#pragma execution_character_set("utf-8")
```

这样可以确保在 Visual Studio 和其他 MSVC 编译器中正确显示中文字符。

### 3. 移除平台相关代码
- 删除了 `system("chcp 65001")` 等平台特定的控制台编码设置代码
- 使用编译器指令代替运行时设置，更加通用

## 文件统计

- 处理文件总数：42 个
- 包含中文的文件：26 个（已添加 pragma 指令）
- 文件类型：.cpp, .h, .hpp

## 使用方法

### 编译和运行
所有文件现在都可以直接在支持 UTF-8 的编译器中编译运行：

```bash
# 使用 g++ 编译（Linux/Mac）
g++ your_file.cpp -o output

# 使用 clang++ 编译
clang++ your_file.cpp -o output

# 使用 MSVC 编译（Windows Visual Studio）
cl your_file.cpp
```

### 跨平台注意事项
- **Linux/macOS**: 大多数现代终端默认支持 UTF-8，无需额外配置
- **Windows (cmd/PowerShell)**: 确保控制台使用 UTF-8 代码页（现代 Windows 版本默认已是）
  - 可选：在运行程序前执行 `chcp 65001`
- **Windows (Visual Studio)**: 添加的 pragma 指令会自动处理编码问题

## 工具脚本

项目中包含了编码修复脚本 `fix_encoding.py`，可以重新处理文件：

```bash
python3 fix_encoding.py
```

该脚本会：
1. 检测文件编码
2. 转换为 UTF-8
3. 统一换行符为 LF
4. 为含中文的文件添加 pragma 指令
5. 移除平台特定的 chcp 调用

## 编码对照

| 编码 | 说明 |
|------|------|
| UTF-8 | 通用 Unicode 编码，支持所有语言字符 |
| GBK/GB2312 | 中文编码（已弃用，可能导致乱码） |
| ASCII | 英文字符编码 |

## 常见问题

### Q: 为什么还有乱码？
A: 检查以下几点：
1. 源文件是否为 UTF-8 编码
2. 编译器是否支持 UTF-8 源文件
3. 终端/控制台是否设置为 UTF-8

### Q: pragma 指令在 GCC/Clang 中会报错吗？
A: `#pragma execution_character_set` 是 MSVC 特有的指令，GCC/Clang 会忽略它（不会报错）。

### Q: 如何在 IDE 中显示正确？
A: 确保编辑器的文件编码设置为 UTF-8，大多数现代 IDE（VS Code、CLion 等）会自动检测。

## 文件结构

```
cpp/
├── book-of-cpp/      # C++ 教程示例
├── exercises/        # 练习题
├── LeetCode/         # LeetCode 解答
├── oj/              # 在线评测题目
├── include/         # 头文件
└── fix_encoding.py  # 编码修复脚本
```
