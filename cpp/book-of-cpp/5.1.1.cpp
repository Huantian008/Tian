#include<iostream>
#include<vector>
using namespace std;
int main(){
    vector<int> nums;
    nums.push_back(1);
    nums.push_back(2);
    nums.push_back(3);
    cout<<"遍历vector："<<endl;
    for(int x:nums){
        cout<<x<<"";
    }
    cout<<endl;
    nums.pop_back();
    cout<<"删除后："<<endl;
    for(int x:nums){
        cout<<x<<"";
    }
    cout<<endl;
    return 0;

}