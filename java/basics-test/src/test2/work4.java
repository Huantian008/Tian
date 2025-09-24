package test2;

public class work4 {
    public static class Mankind {
        int sex;
        int salary;

        // 修改：修正花括号位置
        void manOrWorman(int newSex) {
            if (newSex == 1) {
                System.out.println("man");
            } else if (newSex == 0) {
                System.out.println("woman");
            }
        }
    }

    public static class Kids extends Mankind {
        int yearsOld;

        // 修改：修正printAge方法的实现
        void printAge() {
            System.out.println("年龄:" + yearsOld);
        }
    }

    // 修改：将E类的访问修饰符从public static 改为public static
    public static class E {
        public static void main(String[] args) {
            Kids someKid = new Kids();
            someKid.sex = 1;
            someKid.salary = 5000;
            someKid.yearsOld = 28;

            someKid.manOrWorman(someKid.sex);
            someKid.printAge();
        }
    }
}



