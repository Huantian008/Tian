#include<iostream>
#include<vector>
#include<string>
using namespace std;
int main(){
    vector<int>my_enmpty_vector;
    vector<string> my_fruit={"Apple","Banana","Cherry"};
    cout<<"my_fruit的第一个元素是："<<my_fruit[0]<<endl;
    cout<<"my_fruit共有："<<my_fruit.size()<<endl;
    return 0;

}