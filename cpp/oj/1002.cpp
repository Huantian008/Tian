 #include <iostream>
 #include<string>
 using namespace std;
 int main(){
    int T;
    cin>>T;
    for(int i=1;i<=T;++i){
      string A,B;
      cin>>A>>B;
      string sum ="";
      int carry =0;
      int alen=A.size();
      int blen=B.size();
      int p1=alen-1;
      int p2=blen-1;
      while(p1>=0 || p2>=0||carry){
         int x=0,y=0;
         if(p1>=0){
            x=A[p1]-'0';
         }
      }
    return 0;
 }
