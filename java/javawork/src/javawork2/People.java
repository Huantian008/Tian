package javawork2;

public class People {
    protected double weight;
    protected double height;

    public void speakHello() {
        System.out.println("Hello!");
    }

    public void averageHeight() {
        height = 173;
        System.out.println("Average height: " + height);
    }

    public void averageWeight() {
        weight = 70;
        System.out.println("Average weight: " + weight);
    }

    public static void main(String[] args) {
        People base = new People();
        System.out.println("People:");
        base.speakHello();
        base.averageHeight();
        base.averageWeight();

        System.out.println();

        ChinaPeople china = new ChinaPeople();
        System.out.println("ChinaPeople:");
        china.speakHello();
        china.averageHeight();
        china.averageWeight();
        china.chinaGongfu();

        System.out.println();

        JiangXiPeople jiangXi = new JiangXiPeople();
        System.out.println("JiangXiPeople:");
        jiangXi.speakHello();
        jiangXi.averageHeight();
        jiangXi.averageWeight();
        jiangXi.jiangxiTese();

        System.out.println();

        NanChang nanChang = new NanChang();
        System.out.println("NanChang:");
        nanChang.speakHello();
        nanChang.averageHeight();
        nanChang.averageWeight();
        nanChang.jiangxiTese();
        nanChang.delicacy();
    }
}

class ChinaPeople extends People {
    @Override
    public void speakHello() {
        System.out.println("Hello from China!");
    }

    @Override
    public void averageHeight() {
        height = 185;
        System.out.println("Average height: " + height);
    }

    @Override
    public void averageWeight() {
        weight = 128;
        System.out.println("Average weight: " + weight);
    }

    public void chinaGongfu() {
        System.out.println("Chinese kung fu demo: sit straight, stand firm, sleep soundly.");
    }
}

class JiangXiPeople extends ChinaPeople {
    @Override
    public void speakHello() {
        System.out.println("Hello from Jiangxi!");
    }

    @Override
    public void averageHeight() {
        height = 183;
        System.out.println("Average height: " + height);
    }

    @Override
    public void averageWeight() {
        weight = 121;
        System.out.println("Average weight: " + weight);
    }

    public void jiangxiTese() {
        System.out.println("Jiangxi highlights: Tengwang Pavilion, Lushan, Longhu Mountain, Jinggang Mountain.");
    }
}

class NanChang extends JiangXiPeople {
    public void delicacy() {
        System.out.println("Famous dish: Nanchang mixed rice noodles.");
    }
}
