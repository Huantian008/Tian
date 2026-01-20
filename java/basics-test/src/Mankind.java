public class Mankind {
    private int sex;    // 1 = male, 0 = female
    private int salary; // monthly salary

    public void setSex(int sex) {
        if (sex != 0 && sex != 1) {
            throw new IllegalArgumentException("sex must be 0 (female) or 1 (male)");
        }
        this.sex = sex;
    }

    public void setSalary(int salary) {
        this.salary = salary;
    }

    public void describeGender() {
        System.out.println(sex == 1 ? "man" : "woman");
    }

    public void describeSalary() {
        System.out.println("salary: " + salary);
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

        someKid.describeGender();
        someKid.describeSalary();
        someKid.printAge();
    }
}
