#include<iostream>
#include<vector>
#pragma execution_character_set("utf-8")
//这是用暴力遍历的
using namespace std;
class Solution{
    public:
    vector<int>towSum(vector<int>&nums,int target){
        int n=nums.size();
        for(int i=0;i<n;i++){
            for(int j=i+1;j<n;j++){
                if(nums[i]+nums[j]==target){
                    return{i,j};
                }

            }
            return{};
        }

    }
};
int main(){
    Solution solution;
 vector<int> nums={2,7,11,15};
 int target =9;
 vector<int>result=solution.towSum(nums,target);
 if (!result.empty()) {
        std::cout << "Indices: [" << result[0] << ", " << result[1] << "]" << std::endl;
    } else {
        std::cout << "No two sum solution found." << std::endl;
    }
 return 0;
}