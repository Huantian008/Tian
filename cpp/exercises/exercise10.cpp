#include<iostream>
#include<vector>
#include<memory>
using namespace std;
class Animal{
    public:
    virtual void speak()=0;
    virtual~Animal(){}
};
class Dog:public Animal{
    private:
    int*data;
    public:
    Dog(){
        data=new int[100];
    }
    void speak()override{
        cout<<"大狗叫"<<endl;
    }
    ~Dog(){
        delete[]data;
    }

};
class Cat:public Animal{
    private:
    int*hajimi;
    public:
    Cat(){
        hajimi=new int[200];
    }
    void speak()override{
        cout<<"哈基米"<<endl;
    }
    ~Cat(){
        delete[]hajimi;
    }
};
int main(){
   vector<unique_ptr<Animal>>zoo;
   zoo.push_back(make_unique<Dog>());
   zoo.push_back(make_unique<Cat>());
   for(auto& animal:zoo){
    animal->speak();
   }
    return 0;
}
