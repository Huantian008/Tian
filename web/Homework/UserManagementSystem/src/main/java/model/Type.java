package model;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;

public class Type {
    private int id;
    private String name;
    private String encodeName;

    public Type() {
    }

    public Type(int id, String name) {
        this.id = id;
        setName(name);
    }

    public Type(String name) {
        setName(name);
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
        try {
            this.encodeName = URLEncoder.encode(name == null ? "" : name, "utf-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            this.encodeName = name;
        }
    }

    public String getEncodeName() {
        return encodeName;
    }

    public void setEncodeName(String encodeName) {
        this.encodeName = encodeName;
    }
}
