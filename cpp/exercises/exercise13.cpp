#include<iostream>
#include<vector>
#pragma execution_character_set("utf-8")
using namespace std;
void print_vector(const vector<int>&vec){
    cout<<"Vector 内容";
    for(int i=0;i<vec.size();++i){
        cout<<vec[i]<<" ";
    }
    cout<<"| 当前大小："<<vec.size()<<endl;
}
int main(){
    vector<int>scores;
    
    
    int number;
    cout<<"请输入数字："<<endl;
    while(cin>>number){
        scores.push_back(number);
    }
    cout<<"\n输入的数字是："<<endl;
    print_vector(scores);
    return 0;

}