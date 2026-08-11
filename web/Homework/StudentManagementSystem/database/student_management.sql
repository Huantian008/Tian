drop database if exists student_management_system;
create database student_management_system default character set utf8mb4 collate utf8mb4_unicode_ci;
use student_management_system;

create table admin_user (
    id bigint primary key auto_increment,
    username varchar(50) not null unique comment '登录用户名',
    password varchar(100) not null comment '登录密码',
    real_name varchar(50) not null comment '真实姓名',
    role varchar(30) not null default '管理员' comment '角色'
) comment='管理员用户表';

create table student (
    id bigint primary key auto_increment,
    student_no varchar(30) not null unique comment '学号',
    name varchar(50) not null comment '姓名',
    gender varchar(10) comment '性别',
    age int comment '年龄',
    class_name varchar(80) comment '班级',
    major varchar(100) comment '专业',
    phone varchar(30) comment '电话',
    email varchar(120) comment '邮箱'
) comment='学生信息表';

create table course (
    id bigint primary key auto_increment,
    course_no varchar(30) not null unique comment '课程编号',
    course_name varchar(100) not null comment '课程名称',
    credit decimal(4,1) default 0 comment '学分',
    teacher varchar(50) comment '任课教师',
    semester varchar(30) comment '学期'
) comment='课程信息表';

create table score (
    id bigint primary key auto_increment,
    student_id bigint not null comment '学生ID',
    course_id bigint not null comment '课程ID',
    score decimal(5,1) comment '成绩',
    semester varchar(30) comment '学期',
    constraint fk_score_student foreign key (student_id) references student(id) on delete cascade,
    constraint fk_score_course foreign key (course_id) references course(id) on delete cascade,
    constraint uk_student_course_semester unique (student_id, course_id, semester)
) comment='成绩与选课表';

insert into admin_user(username, password, real_name, role) values
('admin', '123456', '杨文天', '管理员');

insert into student(student_no, name, gender, age, class_name, major, phone, email) values
('202599770425', '杨文天', '男', 22, '23专升本计算机7班', '计算机科学与技术', '13800000001', '202599770425@example.com'),
('202599770401', '李明', '男', 21, '23专升本计算机7班', '计算机科学与技术', '13800000002', 'liming@example.com'),
('202599770402', '王丽', '女', 22, '23专升本计算机7班', '计算机科学与技术', '13800000003', 'wangli@example.com'),
('202599770403', '赵强', '男', 23, '23专升本计算机7班', '计算机科学与技术', '13800000004', 'zhaoqiang@example.com'),
('202599770404', '陈静', '女', 21, '23专升本计算机7班', '计算机科学与技术', '13800000005', 'chenjing@example.com');

insert into course(course_no, course_name, credit, teacher, semester) values
('WEB2026', 'WEB框架技术', 3.0, '肖磊', '2025-2026-2'),
('DB2026', '数据库原理与应用', 3.5, '孙燕敏', '2025-2026-2'),
('JAVA2026', 'Java程序设计', 4.0, '张老师', '2025-2026-2'),
('UI2026', '前端开发技术', 2.5, '刘老师', '2025-2026-2');

insert into score(student_id, course_id, score, semester) values
(1, 1, 92.0, '2025-2026-2'),
(1, 2, 88.5, '2025-2026-2'),
(2, 1, 86.0, '2025-2026-2'),
(2, 3, 90.0, '2025-2026-2'),
(3, 1, 95.0, '2025-2026-2'),
(3, 4, 89.0, '2025-2026-2'),
(4, 2, 82.0, '2025-2026-2'),
(5, 3, 91.5, '2025-2026-2');

