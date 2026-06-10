CREATE DATABASE IF NOT EXISTS homework9 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE homework9;

DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS admin_user;

CREATE TABLE admin_user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_no VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    age INT NOT NULL,
    class_name VARCHAR(100) NOT NULL,
    phone VARCHAR(30)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO admin_user (username, password) VALUES
('admin', '123456');

INSERT INTO student (student_no, name, gender, age, class_name, phone) VALUES
('2026001', '张三', '男', 20, '23计算机专升本7班', '13800138000'),
('2026002', '李四', '女', 21, '23计算机专升本7班', '13900139000'),
('2026003', '王五', '男', 20, '23计算机专升本7班', '13700137000');
