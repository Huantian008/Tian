#include<iostream>
#include<vector>
using namespace std;
int main(){
    int student_count;
    cout<<"请输入学生人数：";
    cin>>student_count;
    vector<int>scores(student_count);
    cout<<"Vector创建成功，大小为："<<scores.size()<<endl;
    if(student_count>0){
        scores[0]=99;
        cout<<"第一个学生的分数被设置为："<<scores[0]<<endl;
    }
    return 0;
}