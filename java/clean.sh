#!/bin/bash

echo "开始清理 Java 项目..."

# 删除所有 out 目录
find . -type d -name "out" -exec rm -rf {} + 2>/dev/null
echo "已删除所有 out 目录"

# 删除所有 out_tmp 目录
find . -type d -name "out_tmp" -exec rm -rf {} + 2>/dev/null
echo "已删除所有 out_tmp 目录"

# 删除所有 .class 文件
find . -type f -name "*.class" -delete
echo "已删除所有 .class 文件"

# 删除所有 bin 目录（如果有）
find . -type d -name "bin" -exec rm -rf {} + 2>/dev/null
echo "已删除所有 bin 目录"

echo "清理完成！"
