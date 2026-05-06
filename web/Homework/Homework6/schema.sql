CREATE DATABASE IF NOT EXISTS homework6 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE homework6;

DROP TABLE IF EXISTS student;

CREATE TABLE student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_no VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    class_name VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO student (student_no, name, age, class_name) VALUES
('2026001', '张三', 20, '23计算机专升本7班'),
('2026002', '李四', 21, '23计算机专升本7班');
