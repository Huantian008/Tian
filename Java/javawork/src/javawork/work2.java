package javawork;

public class work2 {
	public static void main(String[] args) {
	int sum=0,n=1,item=1;
	while(n+item<=9999) {
		sum=sum+item;
		n++;
		item*=n;
	}
	
System.out.println("awnser"+(n-1));
}
}
