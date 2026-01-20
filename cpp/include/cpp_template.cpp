/**
 * C++ 程序模板 - 支持中文输出
 * 
 * 使用说明：
 * 1. 复制这个模板创建新的C++文件
 * 2. 确保文件以UTF-8编码保存
 * 3. 编译时使用：g++ -fexec-charset=UTF-8 文件名.cpp -o 输出名.exe
 * 
 * 作者：[你的名字]
 * 日期：[日期]
 */

#include <iostream>
#include "../include/utf8_console.hpp"
using namespace std;

int main() {
    // 初始化UTF-8控制台支持（必须在第一行）
    init_utf8_console();
    
    // ========== 在这里开始写你的代码 ==========
    
    cout << "你好，世界！" << endl;
    cout << "这是一个支持中文输出的C++程序模板" << endl;
    
    // 示例：输入输出
    string name;
    cout << "请输入你的名字：";
    cin >> name;
    cout << "你好，" << name << "！" << endl;
    
    // ========== 代码结束 ==========
    
    return 0;
}
