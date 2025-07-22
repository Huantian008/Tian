package javawork2;

public class People {
	 public static void main(String[] args) {}
	 
	protected double weight,height;

	  public void speakHello() {

	     System.out.println("yayayaya");

	  } 

	  public void averageHeight() {

	      height=173;

	      System.out.println("average height:"+height);

	  }

	  public void averageWeight() {

	     weight=70;

	     System.out.println("average weight:"+weight);

	  }
}
 class ChinaPeople extends People{
	 public void speakHello() {
		 System.out.println("喵喵喵");
	 }
	 public void averageHeight() {

	      height=185;

	      System.out.println("average height:"+height);

}
   public void averageWeight() {

     weight=128;

     System.out.println("average weight:"+weight);

  }
   public void chinaGongfu() {

       System.out.println("我是中国人，我会中国功夫：坐如钟,站如松,睡如弓");

    }
 }
 class JiangXiPeople extends ChinaPeople{
	 public void speakHello() {

	     System.out.println("组犀利");

	  } 

	  public void averageHeight() {

	      height=183;

	      System.out.println("average height:"+height);

	  }

	  public void averageWeight() {

	     weight=121;

	     System.out.println("average weight:"+weight);

	  }
	  public void jiangxiTese() {

	       System.out.println("我是江西人，我大江西风景名胜：滕王阁、庐山、龙虎山、三清山、明月山、井冈山");

	   }
	 
 }
 class NanChang extends JiangXiPeople {
	 public void delicacy() {
		 System.out.println("南昌拌粉");

	 }
	 
 }
 