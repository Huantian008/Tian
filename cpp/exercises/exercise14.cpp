#include <iostream>
#include <string>
#include "../include/utf8_console.hpp"
#pragma execution_character_set("utf-8")
using namespace std;

int main() {
    ensure_utf8_console();

    string slogan = "I love C++";
    cout << "Slogan: " << slogan << endl;

    string address;
    cout << "\n请输入你的网址：";
    getline(cin, address);
    cout << "你的网址是：" << address << endl;
    return 0;
}
