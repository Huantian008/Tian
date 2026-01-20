#include<iostream>
#pragma execution_character_set("utf-8")
void swap(int& a,int& b){
    int change=a;
    a=b;
    b=change;

}
int main(){
   int x=10,y=20;
   std::cout<<"交换前：x="<<x<<",y="<<y<<std::endl;
   swap(x,y);
   std::cout<<"交换后：x="<<x<<".y="<<y<<std::endl;


    return 0;
}