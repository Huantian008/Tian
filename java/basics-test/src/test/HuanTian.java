package test;

public class HuanTian {
	public static void main(String[ ]args) {
		int a =10, b= 20;
		swap(a,b);
		System.out.println("a="+a+",b="+b);
	}
		public static void swap(int x,int y) {
			int temp =x;
					x=y;
					y=temp;
					
		}
		
	}


