#include<iostream>
#pragma execution_character_set("utf-8")
using namespace std;
int main(){
    int scores[5]={98,87,92,79,85};
    int*p_scores=scores;
    cout<<"数组表示法:"<<scores[1]<<endl;
    cout<<"指针运算"<<*(p_scores+1)<<endl;
    cout<<"指针上的数组表示法"<<p_scores[1]<<endl;
    cout<<"打印整个数组"<<endl;
    for(int i=0;i<5;i++){
        cout<<scores[i]<<endl;
    }
    return 0;
}