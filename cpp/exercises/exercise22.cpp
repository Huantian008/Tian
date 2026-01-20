#include <iostream>
#include "../include/utf8_console.hpp"
#pragma execution_character_set("utf-8")
using namespace std;

int main() {
    init_utf8_console();  // 初始化UTF-8支持，解决中文乱码
    
    int a;
    cout << "请输入一个数字：";
    cin >> a;
    cout << "你输入的数字是：" << a << endl;
    
    return 0;
}
