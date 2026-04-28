#include<iostream>
using namespace std;

int getFailCount(int arr[],int n){
    int count =0;
    for(int i=0;i<n;i++){
        if(arr[i]<60){
            count++;
        }
    }
    return count;
}
double getAvage(int arr[],int n){
    int sum=0;
    int avageNumber=0;
    for(int i=0;i<n;i++){
         sum=arr[i]+sum;
    }
    double avage=sum*1.0/n;
    for(int i=0;i<n;i++){
        if(arr[i]>avage){
            avageNumber++;
        }
    }
    return avageNumber;
}
int findFirstFullMark(int arr[], int n){
    for(int i=0;i<n;i++){
        if(arr[i]==100){
            return i;
        }
        }
        return -1;
    }
   

int main(){
    int score[]={80,100,90,100,70};
    cout<<"不及格人数"<<getFailCount(score,5)<<endl;
    cout<<"大于平均分的人数"<<getAvage(score,5)<<endl;
    cout<<"第一个满分的位置"<<findFirstFullMark(score,5)<<endl;
    return 0;
}