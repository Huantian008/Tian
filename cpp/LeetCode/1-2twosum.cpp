#include <iostream>
#include<vector>
#include<unordered_map>
#pragma execution_character_set("utf-8")
//哈希表写的
using namespace std;
class Solution{
public:
vector<int>twoSum(vector<int>&nums,int target){
    unordered_map<int,int>map;
    for(int i=0;i<nums.size();++i){
        int complement =target -nums[i];
        if(map.count(complement)){
            return{map[complement],i};

        }
        map[nums[i]]=i;
    }
    return{};
}
};
int main(){
    Solution soulution;
    vector<int>nums={2,7,11,15};
    int target =9;
    vector<int> result=soulution.twoSum(nums,target);
    if(!result.empty()){
        cout<<"Indices:["<<result[0]<<","<<result[1]<<"]"<<endl;
    }
    return 0;
}