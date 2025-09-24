package javawork;

public class work4 {
    public static class Mankind {
        int sex;
        int salary;

        void manOrWoman(int newSex) {
            if (newSex == 1) {
                System.out.println("男性");
            } else if (newSex == 0) {
                System.out.println("女性");
            }
        }
    }

    public static class Kids extends Mankind {
        int yearsOld;

        void printAge() {
            System.out.println("年龄:" + yearsOld);
        }
    }

    public static class E {
        public static void main(String[] args) {
            Kids someKid = new Kids();
            someKid.sex = 1;
            someKid.salary = 5000;
            someKid.yearsOld = 28;
            someKid.manOrWoman(someKid.sex);
            someKid.printAge();
        }
    }
}
