while True:
    student_id = input("请输入您的学号：")
    
    if len(student_id) != 12:
        print("您输入的学号位数不对，请重新输入：", student_id)
        continue 
    else:
        break  

if student_id[4:8] == "9977":
    print(f"学号为{student_id}的学生是计算机科学系的学生")
else:
    print(f"学号为{student_id}的学生不是计算机科学系的学生")
