#include<iostream>
#pragma execution_character_set("utf-8")
using namespace std;
int main(){
    int n;
    cout<<"请输入数组大小";
     cin>>n;
     int*arr=new int[n];
     for(int i=0;i<n;i++){
        arr[i]=i*3;
        cout<<arr[i]<<" ";
     }
     cout<<endl;
     delete[]arr;
     return 0;
}