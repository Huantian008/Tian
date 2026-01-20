package javawork;

public class work4 {
    private static class Mankind {
        private int sex;
        private int salary;

        public void setSex(int sex) {
            this.sex = sex;
        }

        public void setSalary(int salary) {
            this.salary = salary;
        }

        public void printGender() {
            System.out.println(sex == 1 ? "male" : "female");
        }
    }

    private static final class Kid extends Mankind {
        private int yearsOld;

        public void setYearsOld(int yearsOld) {
            this.yearsOld = yearsOld;
        }

        public void printAge() {
            System.out.println("age: " + yearsOld);
        }
    }

    public static void main(String[] args) {
        Kid someKid = new Kid();
        someKid.setSex(1);
        someKid.setSalary(5_000);
        someKid.setYearsOld(28);

        someKid.printGender();
        someKid.printAge();
    }
}
