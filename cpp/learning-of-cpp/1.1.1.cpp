#include<iostream>
using namespace std;

bool contains(int arr[],int n,int target){
    for(int i=0;i<n;i++){
        if(arr[i]==target){
            return true;
        }
    }
    return false;
}
int main(){
    int scores[5];
    int target;
    cout<<"输入五名学生的成绩"<<endl;
    for(int i=0;i<5;i++){
        cin>>scores[i];
    }
    cout<<"请输入要查找的成绩"<<endl;
    if(contains(scores,5,target)){
        cout<<"找到了"<<endl;
    }else{
        cout<<"没找到"<<endl;
    }
    return 0;

}