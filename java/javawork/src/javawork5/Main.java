package javawork5;

import java.io.*;

public class Main {
    public static void main(String[] args) {

        String clazz = "23专升本计算机7班";
        String name = "杨文天";
        String gender = "男";
        String id = "202599770425";

        try (
                FileWriter fw = new FileWriter("info.txt");
                BufferedWriter bw = new BufferedWriter(fw)
        ) {
            bw.write("班级：" + clazz);
            bw.newLine();

            bw.write("姓名：" + name);
            bw.newLine();

            bw.write("性别：" + gender);
            bw.newLine();

            bw.write("学号：" + id);
            bw.newLine();

            System.out.println("写入完成！");
        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("\n文件内容读取如下：");

        try (
                FileReader fr = new FileReader("info.txt");
                BufferedReader br = new BufferedReader(fr)
        ) {
            String line;
            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
