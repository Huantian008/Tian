#include <iostream>
#include <random>
#include <ctime>
#include "../include/utf8_console.hpp"
#pragma execution_character_set("utf-8")
using namespace std;

int main() {
    ensure_utf8_console();

    // 使用当前时间生成随机数种子
    random_device rd;         // 硬件随机数生成器
    mt19937 gen(rd());        // 梅森旋转算法产生器

    // 定义随机数范围（1 ~ 100）
    uniform_int_distribution<> dis(1, 100);

    cout << "=== 随机数生成器 ===" << endl;
    cout << "生成10个随机数（范围：1-100）：" << endl;

    // 生成并输出10个随机数
    for (int i = 0; i < 10; i++) {
        int random_num = dis(gen);
        cout << "随机数 " << i + 1 << ": " << random_num << endl;
    }

    cout << "\n按回车键生成一个新的随机数..." << endl;
    cin.get();

    // 生成一个新的随机数
    int new_random = dis(gen);
    cout << "新的随机数: " << new_random << endl;

    return 0;
}
