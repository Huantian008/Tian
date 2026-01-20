#include<iostream>
#include<string>
#include<memory>
#pragma execution_character_set("utf-8")
class Animal{
    public:
   
    void eat(const std::string&food=""){
         if(food.empty()){
            std::cout<<"I am not eating "<<std::endl;
         }else{
            std::cout<<"I am eating "<<food<<"."<<std::endl;

         }
        }
};
class Dog:public Animal{
    public:
    void bark(){std::cout<<"Woof!"<<std::endl;}
};
void useResource(){
    std::unique_ptr<int> p_smart_int(new int (200));
    *p_smart_int =250;
    std::cout<<*p_smart_int<<std::endl;
}
int main(){
    using namespace std;
    string food;
    cout<<"请输入你今晚吃了什么\n";
    cin>>food;
useResource();
auto smartAnimal =std::make_unique<Animal>();
smartAnimal->eat(food); 
auto smartDog =std::make_unique<Dog>();
smartDog->bark();
return 0 ;
}