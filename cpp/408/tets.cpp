#include<iostream>
using namespace std;
int main(){
    int n;
    cout<<"请输入有几个数字"<<endl;
    cin>>n;
    int x;
    cout<<"请输入数字"<<endl;
    cin>>x;
    int Maxn=x;
    for(int i=1;i<n;i++){
        cin>>x;
        if(x>Maxn){
            Maxn=x;
        }
    }
    cout<<Maxn<<endl;
    return 0;
}
