#include<iostream>
using namespace std;
int getMax(int arr[],int n){
    int maxValue =arr[0];
    for (int i = 0; i < n; i++)
    {
        if(arr[i]>maxValue)
        maxValue=arr[i];
    }
    return maxValue;
}
int getMin(int arr[],int n){
    int minValue =arr[0];
    for(int i=0;i<n;i++){
        if(arr[i]<minValue){
            minValue=arr[i];
        }
    }
    return minValue;
}
double getAverage(int arr[],int n){
    int sum=0;
    for(int i=0;i<n;i++){
        sum += arr[i];
    }
    return sum*1.0/n;
}
int getPasscount(int arr[],int n){
    int count=0;
    for(int i=0;i<n;i++){
        if(arr[i]>=60){
            count++;
        }
    }
    return count;
}
int main(){
    int n;
   cout<<"有多少个学生"<<endl;
    cin>>n;
     int scores[n];
     cout<<"学生的成绩是多少"<<endl;
     cin>>scores[n];
    for(int i=0;i<n;i++){
        cin>>scores[i];
    }
    cout<<"最高分"<<getMax(scores,n)<<endl;
    cout<<"最低分"<<getMin(scores,n)<<endl;
    cout << "平均分：" << getAverage(scores, n) << endl;
    cout << "及格人数：" << getPasscount(scores, n) << endl;
    return 0;
}