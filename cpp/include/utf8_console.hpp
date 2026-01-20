#pragma once

#ifdef _WIN32
#include <windows.h>
#include <iostream>
#pragma execution_character_set("utf-8")
#endif

/**
 * @brief 初始化控制台以支持UTF-8编码
 * 
 * 这个函数会设置Windows控制台的输入输出代码页为UTF-8，
 * 解决中文输出乱码问题。
 * 
 * 使用方法：在main函数开头调用此函数
 * 
 * @note 仅在Windows系统上有效，其他系统会自动忽略
 */
inline void init_utf8_console() {
#ifdef _WIN32
    // 设置控制台输出代码页为UTF-8
    SetConsoleOutputCP(CP_UTF8);
    // 设置控制台输入代码页为UTF-8
    SetConsoleCP(CP_UTF8);
    // 同步C++流与C标准流，确保输出正确
    std::ios::sync_with_stdio(false);
#endif
}

// 为了兼容旧代码，保留旧函数名
inline void ensure_utf8_console() {
    init_utf8_console();
}
