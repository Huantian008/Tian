#include <stdio.h>

int printSquare(int number){
	int get = number * number;
printf("%d%d\n",number,get);
return get;
}
int add(int a,int b){
    return a+b;

}
int main(){
    int a05= printSquare(5);
    int a08=printSquare(8);
    int a07=printSquare(7);
    printf("????????%d\n",a05+a07+a08);
    return 0;
}