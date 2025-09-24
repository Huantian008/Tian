package javawork3;

public class Building {
private String name;
private String style;
public Building() {
	this("鸟巢","现代");
}
public Building (String name,String style) {
	this.name=name;
	this.style=style;
}
public void setName(String name) {
	this.name=name;
}
public String getName() {
	return name;
}
public void setStyle(String style) {
	this.style=style;
}
public String getStyle() {
	return style;
}
public void introduce() {
	System.out.println("这座建筑名叫"+name);
	System.out.println("风格为"+style);
}
}
