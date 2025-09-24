#include<string>
#include<iostream>
#include<algorithm>
using namespace std;
class Solution_String{
public:
bool isPalindrome(int x){
    if(x<0){
        return false;
    }
    string s=to_string(x);
    int left =0;
    int right =s.length()-1;
     while(left<right){
        if(s[left]!=s[right]){
            return false;
        }
        left++;;
        right--;
     }
     return true;
}
};