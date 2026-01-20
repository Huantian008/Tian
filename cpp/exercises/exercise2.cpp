#include<iostream>
#include<string>
#include<vector>
#pragma execution_character_set("utf-8")
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
           std::string tempName;
           int tempID;
           double tempScore;
           std::cout<<"请输入学生姓名：";
           std::cin>>tempName;
           std::cout<<"请输入学生学号：";
           std::cin>>tempID;
           std::cout<<"请输入学生分数：";
           std::cin>>tempScore;
           Student newstudent;
           newstudent.name=tempName;
           newstudent.score=tempScore;
           newstudent.studentID=tempID;
           roster.push_back(newstudent);
           std::cout<<"学生信息添加成功！\n";

        }else if(number==2){
            if(roster.size()==0){
                std::cout<<"当前名册为空\n";
            }else{
                for (size_t i = 0; i < roster.size(); ++i)
                {
                    
                    roster[i].displayInfo();
                }
            }
                

                }
                else if(number==3){
                    std::cout<<"感谢使用，再见";
                    break;

                }
            }
            return 0;

        }
        
    
    
    
