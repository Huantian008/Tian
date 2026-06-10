CREATE DATABASE IF NOT EXISTS homework7 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE homework7;

DROP TABLE IF EXISTS user_info;

CREATE TABLE user_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    real_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    age INT NOT NULL,
    phone VARCHAR(30) NOT NULL,
    email VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO user_info (username, password, real_name, gender, age, phone, email, address) VALUES
('zhangsan', '123456', '张三', '男', 20, '13800138000', 'zhangsan@example.com', '北京市海淀区'),
('lisi', '123456', '李四', '女', 21, '13800138001', 'lisi@example.com', '上海市浦东新区');
