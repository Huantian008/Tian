#include<iostream>
#include<string>
 using namespace std;
 int main(){
    string slogan="I love C++";
    cout<<"Slogan:"<<slogan<<endl;
    string address;
    cout<<"\n请输入你的网址";
    getline(cin,address);
    cout<<"你的网址是"<<address<<endl;
    return 0;
 }