#!/bin/bash

echo "清理 C++ 临时文件..."

# 清理可执行文件
find ./cpp -type f \( -name "*.exe" -o -name "*.out" -o -name "a.out" \) -exec rm -f {} \;
echo "已删除可执行文件"

# 清理编译输出文件
find ./cpp -type f \( -name "*.o" -o -name "*.obj" \) -exec rm -f {} \;
echo "已删除目标文件"

# 清理 output 目录（保留目录结构）
for dir in ./cpp/exercises/output ./cpp/LeetCode/output ./cpp/oj/output; do
    if [ -d "$dir" ]; then
        rm -rf "${dir:?}"/*
        echo "已清理 $dir"
    fi
done

echo "清理完成！"
