#include<iostream>
#include<string>
#pragma execution_character_set("utf-8")
using namespace std;
void hanoi(int n,
    const string &start,
    const string &middle,
    const string &end
){
    if(n==1){
        cout<<"把第1口铜钟：从"<<start<<"->"<<end << endl;
        return;
    }
    hanoi(n-1,start,end,middle);
    cout<<"把第"<<n<<"口铜钟：从"<<start<<"->"<<end<<endl;
    hanoi(n-1,middle,start,end);
}
int main(){
    int n=3;
    hanoi(n,"城东","城中","城西");
    return 0;
}