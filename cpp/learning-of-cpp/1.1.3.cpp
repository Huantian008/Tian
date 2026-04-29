#include<iostream>
#include<vector>
using namespace std;
int getFailCount(const vector<int>&secores  ){
    int count=0;
    for(int i=0;i<secores.size();i++){
        if(secores[i]<60){
            count++;
        }
    }
    return count;
}
int getAboveAverageCount(const vector<int>&secores){
    int sum=0;
    double averagae=0;
    for(int i=0;i<secores.size();i++){
        sum=secores[i]+sum;
    }
    averagae =1.00*sum/secores.size();
    int count =0;
    for(int i=0;i<secores.size();i++){
        if(secores[i]>averagae){
            count++;
        }
    }
    return count;
}
int findFirstFullMark(const vector<int>&secores){
    for(int i=0;i<secores.size();i++){
        if(secores[i]==100){
            return i;
        }
    }
    return -1;
}
int main(){
    vector<int>scores{80, 100, 90, 100, 70};
    cout << "不及格人数：" << getFailCount(scores) << endl;
    cout << "大于平均分的人数：" << getAboveAverageCount(scores) << endl;
    cout << "第一个满分的位置：" << findFirstFullMark(scores) << endl;
return 0;
}
