#include<stdarg.h>
#include<stdio.h>
void test(int tot,...){
    va_list valist;
    int i;
    va_start(valist,tot);
    for(i=0;i<tot;++i){
        double xx=va_arg(valist,double);
        printf("i=%d,value=0x%016llx\n",i,*(long long *)(&xx));
    }
    va_end(valist);
}
int main(){
    float f,a;
    double fd,d,c;
    f=123.;
    fd=123.;
    d=456.;
    a=789;
    c=901;
    test(5,f,fd,d,a,c);
}