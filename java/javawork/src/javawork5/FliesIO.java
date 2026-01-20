package javawork5;

import java.io.*;

public class FliesIO {
    public static void main(String[] args) throws IOException {
        InputStream in = new FileInputStream("javawork5/Blue Achieve paper1.png");
        OutputStream out = new FileOutputStream("image");

        byte[] buffer = new byte[1024];
        int length;

        while ((length = in.read(buffer)) != -1) {
            out.write(buffer, 0, length);
        }

        in.close();
        out.close();

    }
}
