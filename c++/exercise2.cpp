#include<iostream>
#include<string>
#include<vector>
 class Student
{
public:
    std::string name;
    int studentID;
    double score;
    void displayInfo(){
        std::cout<< name<<std::endl;
        std::cout<<studentID<<std::endl;
        std::cout<<score<<std::endl;

    }
};

int main(){
    system("chcp 65001");
    std::vector<Student> roster;
    int number;
    while (true)
    {
        std::cout<<"学生名册管理系统"<<std::endl;
        std::cout<<"1.添加新学生"<<std::endl;
        std::cout<<"2.显示所有学生"<<std::endl;
        std::cout<<"3.退出程序"<<std::endl;
        std::cout<<"请选择您的操作："<<std::endl;
        std::cin>>number;
        if (number==1)
        {
            std::cout<<"请依次输入新学生的姓名、学号、分数。"<<std::endl;
            Student student;
            student.name;
            student.score;
        }
        
    }
    
    return 0;
}