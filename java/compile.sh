#!/bin/bash

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
    echo "用法: ./compile.sh <项目名称>"
    echo ""
    echo "可用项目:"
    echo "  basics-test    - 基础测试"
    echo "  exercise2      - 练习 2"
    echo "  hello-intellij - IntelliJ 入门"
    echo "  javawork       - Java 练习作业"
    echo "  oop-practice   - OOP 练习"
    echo ""
    echo "或使用 'all' 编译所有项目"
    exit 1
fi

if [ "$PROJECT_NAME" = "all" ]; then
    echo "编译所有项目..."
    for dir in basics-test exercise2 hello-intellij javawork oop-practice; do
        if [ -d "$dir" ]; then
            echo ""
            echo "=== 编译 $dir ==="
            cd "$dir"
            rm -rf out
            mkdir -p out
            javac -d out $(find src -name '*.java' 2>/dev/null)
            cd ..
        fi
    done
    echo ""
    echo "所有项目编译完成！"
else
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
fi
