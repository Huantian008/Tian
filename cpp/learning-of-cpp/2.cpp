#include<iostream>
#include<string>
#include<vector>
using namespace std;

struct Student
{
    string name;
    int id;
    int score;
};
int main(){
    Student stu;
    vector<Student>students={
        {"张三",1001,80},
        {"李四",1002,100},
        {"王五",1003,90},
        {"哈基米",1004,100}
    };
    cout<<"学号"<<stu.id<<endl;
    cout<<"姓名"<<stu.name<<endl;
    cout<<"成绩"<<stu.score<<endl;
    return 0;
}
