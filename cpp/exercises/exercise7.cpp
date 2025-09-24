#include<iostream>
int main(){
    using namespace std;
    int dayOfWeek ;
    cout<<"请输入星期几："<<endl;
    cin>>dayOfWeek;
    switch (dayOfWeek)
    {
    case 1:
        cout<<"Monday"<<endl;
        break;
    case 2:
    cout<<"Tuesday"<<endl;
    break;
    case 3:
    cout<<"wednesday"<<endl;
    break;
    case 4:
    cout<<"Thursday"<<endl;
    break;
    case 5:
    cout<<"Friday"<<endl;
    break;
    default:
        break;
    }
}