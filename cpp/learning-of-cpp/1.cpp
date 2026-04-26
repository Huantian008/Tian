#include<iostream>
using namespace std;
int main(){
    int scores[5];
    cout<<"定义5个学生的成绩："<<endl;
    for (int i=0;i<5;i++){
        cin>>scores[i];
    }
    int maxScore=scores[0];
    int minScore=scores[0];
    int sum=0;
    int passCount =0;
    for(int i=0;i<5;i++){
        if(scores[i]>maxScore){
            maxScore=scores[i];
        }
        if (scores[i]<minScore)
        {
            minScore=scores[i];
        }
        sum +=scores[i];
        if (scores[i]>=60)
        {
            passCount++;
        }
    }
    double average=sum*1.0/5;
    cout<<"最高分"<<maxScore<<endl;
    cout<<"最低分"<<minScore<<endl;
    cout<<"总分"<<sum<<endl;
    cout<<"平均分"<<average<<endl;
    return 0;
}