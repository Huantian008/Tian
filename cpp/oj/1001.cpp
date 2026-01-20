#include <iostream>
#pragma execution_character_set("utf-8")

int main()
{
    using namespace std;
   long x;
   cout<<"请输入起始数字：";
   cin>>x;
   long y;
   cout<<"请输入项数";
   cin>>y;
   long sum=(y*(x+y))/2;
   cout<<"计算结果"<<sum;

    return 0;
}