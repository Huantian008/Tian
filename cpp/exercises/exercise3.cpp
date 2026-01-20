#include<iostream>
#include<vector>
#include<string>
#pragma execution_character_set("utf-8")
int main(){
   std::vector<double> scores;
   double number;
   while(true){
    std::cout<<"请输入成绩\n";
    std::cin>>number;
    
    if (number==-1)
    {
        break;
    }
    scores.push_back(number);
   }
    if(scores.empty()){
        std::cout<<"没有输入任何成绩\n";
    }else{

        double maxScore=scores[0];
        for (const auto&score:scores)
        {
            if(score>maxScore){
                maxScore=score;
            }
        }
        std::cout<<"最高成绩是："<<maxScore<<std::endl;
        
    }
    return 0;
}