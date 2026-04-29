#include<iostream>
#include<vector>
using namespace std;
int getMaxScore(const vector<int>&scores){
    int MaxScore=scores[0];
    for(int i=0;i<scores.size();i++){
        if(scores[i]>MaxScore){
            MaxScore=scores[i];
        }
    }
    return MaxScore;
}
int getMinScores(const vector<int>&scores){
    int MinScores=scores[0];
    for(int i=0;i<scores.size();i++){
        if(scores[i]<MinScores){
            MinScores=scores[i];
        }
    }
    return MinScores;
}
int getFullMarkCount(const vector<int>& scores){
    int count=0;
    for(int i=0;i<scores.size();i++){
        if(scores[i]==100){
            count++;
        }
    }
    return count;
}
int findFirstScore(const vector<int>& scores, int target){
    for(int i=0;i<scores.size();i++){
        if(scores[i]==target){
            return i;
        }
    }
    return -1;
}
int main(){
    int n;
    vector<int>scores;
    cout<<"请输入学生的人数";
    cin>>n;

    if(n <= 0){
    cout << "学生人数必须大于0" << endl;
    return 0;
}
    for(int i=0;i<n;i++){
        int x;
        cout<<"请输入第"<<i+1<<"个学生的成绩:";
        cin>>x;
        while(x<0||x>100){
            cout<<"成绩不合法，请重新输入1到100之间的成绩";
            cin>>x;
        }
        scores.push_back(x);

    }
    int target;
    cout<<"请输入你想查找的成绩";
    cin>>target;

    cout << "最高分：" << getMaxScore(scores) << endl;
    cout << "最低分：" << getMinScores(scores) << endl;
    cout << "满分人数：" << getFullMarkCount(scores) << endl;
    int pos=findFirstScore(scores, target);
if(pos==-1){
    cout<<"没有找到这个成绩"<<endl;
}else{
    cout<<"这个成绩第一次出现的位置是"<<pos<<endl;
}
    return 0;
}