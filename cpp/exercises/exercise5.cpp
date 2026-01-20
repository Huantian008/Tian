#include<iostream>
#include<vector>
#include<algorithm>
#pragma execution_character_set("utf-8")
int main(){
    std::vector<int>nums={5,2,8,1,9};
    std::sort(nums.begin(),nums.end());
    std::cout<<"排序后的vector:";
    for(const auto&n:nums){
        std::cout<<n<<" ";
    }
    std::cout<<std::endl;
    return 0;
}

