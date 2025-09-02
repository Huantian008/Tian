#include<iostream>
#include<cstdlib> // 为了使用 system() 函数
using namespace std;
int main(){
    system("chcp 936"); // 设置控制台代码页为GBK
    int age=20;
    bool hasLicense =true;
    if(age>=18&&hasLicense){
        cout<<"可以开车"<<endl;
    }else{
        cout<<"不可开车"<<endl;
    }
    bool hasTicket =true;
    bool isExpired=true;
    if(hasTicket&&!isExpired){
        cout<<"门票有效"<<endl;
    }else{
        cout<<"无效"<<endl;
    }
    return 0;
}