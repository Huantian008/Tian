#include<iostream>
using namespace std;
int main(){
    int my_score=95;
    int *p_score=&my_score;
    cout<<"直接访问"<<my_score<<endl;
    cout<<"通过指针访问"<<*p_score<<endl;
    *p_score=100;
    cout<<"修改过后"<<*p_score<<endl;
    return 0;
}