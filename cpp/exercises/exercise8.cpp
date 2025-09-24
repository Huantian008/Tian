#include<iostream>
#include<string>
using namespace std;
void print(int value){
    cout<<"Integer:"<<value<<endl;
}
void print(double value){
    cout<<"Double:"<<value<<endl;
}
void print(const string& value){
    cout<<"String:"<<value<<endl;
}
int main(){
    print(10);
    print(3.14);
    print("Hello");
    return 0;
}