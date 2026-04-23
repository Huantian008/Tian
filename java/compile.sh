#!/bin/bash

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
    echo "用法: ./compile.sh <项目名称>"
    echo ""
    echo "可用项目:"
    echo "  javawork       - Java 练习作业"
    echo ""
    echo "或使用 'all'（等同于 javawork）"
    exit 1
fi

if [ "$PROJECT_NAME" = "all" ]; then
    PROJECT_NAME="javawork"
fi

if [ "$PROJECT_NAME" != "javawork" ]; then
    echo "错误: 仅支持 'javawork' 或 'all'"
    exit 1
fi

if [ ! -d "$PROJECT_NAME" ]; then
    echo "错误: 项目 '$PROJECT_NAME' 不存在"
    exit 1
fi

echo "=== 编译 $PROJECT_NAME ==="
cd "$PROJECT_NAME"
rm -rf out
mkdir -p out
javac -d out $(find src -name '*.java' 2>/dev/null)
cd ..
echo "编译完成！"
