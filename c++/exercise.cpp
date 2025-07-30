#include<iostream>
#include<vector>
int main(){
    system("chcp 65001");
  std::vector<double>numbers;
  double num;
   std::cout<<"请输入一个数字（输入-1表示结束）"<<std::endl;
  while (std::cin >> num) {;
    if (num == -1){
       break;}
    numbers.push_back(num);
    std::cout<<"请输入一个数字（输入-1表示结束）"<<std::endl;
  }
  std::cout<<"正在计算总和..."<<std::endl;
  double totalSum=0.0;
for (int i = 0; i <numbers.size(); i++)
{
 totalSum+=numbers[i];
}
std::cout<<"所有输入数字的总和是："<<totalSum<<std::endl;
return 0;
}
   

