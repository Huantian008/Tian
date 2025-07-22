package javawork;

public class work1 {
	  public static void main(String[] args) {
		int number=496,sum=1;
		for(int i =2;i<=number;i++) {
			if(number % i==0) {
				sum +=i;
				if (i!=number /i) {
					sum+=number/i;
				}
			}
		}
		if((sum==number)) {
		System.out.println(number+"是完数");
		}else {
			System.out.println(number+"不是完数");
		}
}
}