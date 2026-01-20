#include<iostream>
using namespace std;
int main(){
    int T; 
    cin>>T; //测试用例个数
    for (int t=1;t<=T;t++){
        int n;
        cin>>n;  //数组长度

        int a;
        cin>>a;

        int curSum=a;
        int maxSum=a;

        int curlL =1; //当前子段起点
        int bestL =1; //最优子段起点
        int bestR =1; //最优子段终点

        for(int i =2;i<=n;i++){
            cin>>a;

            if(curSum<0){
                curSum=a;
                curlL =i;
            }else{
                curSum=curSum+a;
            }
            if(curSum>maxSum){
                maxSum=curSum;
                bestL=curlL;
                bestR=i;
            }
        }


    }
}