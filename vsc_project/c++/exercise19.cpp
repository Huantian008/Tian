#include<iostream>
using namespace std;
int main(){
    int n;
    cout<<"请输入大小";
    cin>>n;
    int*arr=new int[n];
    for(int i=0;i<n;i++){
        arr[i]=i+1;
    }
    for(int i=0;i<n;i++){
        cout<<arr[i]<<" ";

    }
    cout<<endl;
    delete[]arr;
    return 0;
    
}