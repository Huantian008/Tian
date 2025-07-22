

public class work4 {
	public static class Mankind{
	 int sex;
	 int salary;
	void manOrWorman(int  newSex) {
				if (newSex == 1) {
            System.out.println("man");
        } else if (newSex == 0) {
            System.out.println("woman");
		
	}
}
	public static class kids extends Mankind{
		 int yearsOld;
		void printAge() {
			System.out.println("年龄:"+yearsOld);
		
		}
	}
	
public  static class E{
	public static void main(String[] args) {
		kids somekid=new kids();
		somekid.sex = 1;
        somekid.salary = 5000;
        somekid.yearsOld = 28;
        somekid.manOrWorman(somekid.sex);
        somekid.printAge();
}

	
}
}
	
	}


		
	
