package pack3;
import pack1.A; 
import pack2.B;


public class c {
	public static void main(String[]args){
		int sum =A.add(30);
		System.out.println("1+2+...30的和为:"+sum);
		int factorialResult = B.cheng(10);
        System.out.println("10 的阶乘为：" + factorialResult);
	}
	
}
