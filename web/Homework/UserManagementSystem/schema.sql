CREATE DATABASE IF NOT EXISTS cookieshop DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE cookieshop;

CREATE TABLE IF NOT EXISTS `user` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(45) UNIQUE,
    email VARCHAR(45) UNIQUE,
    password VARCHAR(45),
    name VARCHAR(45),
    phone VARCHAR(45),
    address VARCHAR(45),
    isadmin BIT(1),
    isvalidate BIT(1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `type` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(45)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS goods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(45),
    cover VARCHAR(45),
    image1 VARCHAR(45),
    image2 VARCHAR(45),
    price FLOAT,
    intro VARCHAR(300),
    stock INT,
    type_id INT,
    INDEX idx_goods_type_id(type_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS recommend (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type TINYINT(1),
    goods_id INT,
    INDEX idx_recommend_goods_id(goods_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `order` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    total FLOAT,
    amount INT,
    status TINYINT(1),
    paytype TINYINT(1),
    name VARCHAR(45),
    phone VARCHAR(45),
    address VARCHAR(45),
    datetime DATETIME,
    user_id INT,
    INDEX idx_order_user_id(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS orderitem (
    id INT PRIMARY KEY AUTO_INCREMENT,
    price FLOAT,
    amount INT,
    goods_id INT,
    order_id INT,
    INDEX idx_orderitem_goods_id(goods_id),
    INDEX idx_orderitem_order_id(order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `user` (username, email, password, name, phone, address, isadmin, isvalidate) VALUES
('testuser', 'test@example.com', '123456', '测试用户', '13800000000', '广东省广州市天河区', 0, 1),
('admin', 'admin@example.com', '123456', '管理员', '13900000000', '学校机房', 1, 1)
ON DUPLICATE KEY UPDATE
    password = VALUES(password),
    name = VALUES(name),
    phone = VALUES(phone),
    address = VALUES(address),
    isadmin = VALUES(isadmin),
    isvalidate = VALUES(isvalidate);

INSERT INTO `type` (id, name) VALUES
(1, '冰淇淋系列'),
(2, '零食系列'),
(3, '儿童系列'),
(4, '法式系列'),
(5, '经典系列'),
(8, '节日系列'),
(11, '买不起系列')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO goods (id, name, cover, image1, image2, price, intro, stock, type_id) VALUES
(9, '草莓冰淇淋', '/picture/9-1.jpg', '/picture/9-2.jpg', '/picture/9-3.jpg', 299, '草莓风味冰淇淋蛋糕，口感清爽。', 10, 1),
(10, '玫瑰舒芙蕾', '/picture/10-1.jpg', '/picture/10-2.jpg', '/picture/10-3.jpg', 28, '松软舒芙蕾，带玫瑰香气。', 10, 3),
(11, '半熟芝士', '/picture/11-1.jpg', '/picture/11-1.jpg', '/picture/11-1.jpg', 38, '经典半熟芝士，入口细腻。', 10, 3),
(12, '青森芝士条', '/picture/12-1.jpg', '/picture/12-1.jpg', '/picture/12-1.jpg', 36, '芝士味浓郁，适合作为下午茶。', 10, 2),
(13, '蜂蜜蛋糕', '/picture/13-1.jpg', '/picture/13-1.jpg', '/picture/13-1.jpg', 36, '蜂蜜香甜，口感绵密。', 10, 2),
(14, '法式小蛋糕', '/picture/14-1.jpg', '/picture/14-1.jpg', '/picture/14-1.jpg', 58, '简洁精致的法式甜点。', 10, 4)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    cover = VALUES(cover),
    image1 = VALUES(image1),
    image2 = VALUES(image2),
    price = VALUES(price),
    intro = VALUES(intro),
    stock = VALUES(stock),
    type_id = VALUES(type_id);

INSERT INTO recommend (id, type, goods_id) VALUES
(9, 2, 9),
(10, 3, 10),
(11, 3, 12),
(12, 3, 13),
(29, 1, 9),
(30, 1, 10),
(31, 2, 11),
(32, 2, 14)
ON DUPLICATE KEY UPDATE
    type = VALUES(type),
    goods_id = VALUES(goods_id);
