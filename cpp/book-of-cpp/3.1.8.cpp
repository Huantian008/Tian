#include<iostream>
using namespace std;
int main(){
    for(int i=0;i<128;i++){
        char ch=i;
        cout<<i<<":"<<ch<<" ";
        if(i%5==0)cout<<endl;
    }
    return 0;
}