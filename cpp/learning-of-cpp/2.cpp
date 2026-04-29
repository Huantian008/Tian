#include<iostream>
#include<string>
using namespace std;

struct Student
{
    string name;
    int id;
    int score;
};
int main(){
    Student stu;
    stu.name="张三";
    stu.id=1001;
    stu.score=80;
    cout<<"学号"<<stu.id<<endl;
    cout<<"姓名"<<stu.name<<endl;
    cout<<"成绩"<<stu.score<<endl;
    return 0;
}
