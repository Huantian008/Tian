CREATE DATABASE IF NOT EXISTS studb DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE studb;

DROP TABLE IF EXISTS student;

CREATE TABLE student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    sex VARCHAR(10) NOT NULL,
    address VARCHAR(100) NOT NULL
);

INSERT INTO student (name, age, sex, address) VALUES
('张三', 20, '男', '北京市海淀区'),
('李四', 21, '男', '上海市浦东新区'),
('王芳', 19, '女', '广州市天河区'),
('赵敏', 22, '女', '北京市朝阳区'),
('张伟', 20, '男', '南京市鼓楼区');
