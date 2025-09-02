#include<iostream>
#include<vector>
#include<string>
using namespace std;
int main(){
    vector<int> numbers{ 10,20,30,40,50};
    cout<<"遍历vector\n";
    for(int number:numbers){
        cout<<number<<" ";
    }
    cout<<endl;
string hello="World";
cout<<"遍历 string\n";
for(char c:hello){
    cout<<c<<" ";
}
cout<<endl;
return 0;
}