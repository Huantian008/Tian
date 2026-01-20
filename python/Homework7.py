list1=["201865110102", "李天", "男", 18, 90, 66, 85]
list2=["201865110201", "赵琴", "女", 19, 85, 82, 90]
list3=["201865110202", "王凡", "男", 20, 68, 84, 79]
students=[list1,list2,list3]
print("学生成绩表：")
print("学号\t姓名\t性别\t年龄\t英语成绩\t思政成绩\tPython成绩")
for student in students:
    print("\t".join(map(str,student)))
students[1][6] = 88
print("\n修改后的成绩表")
print("学号\t姓名\t性别\t年龄\t英语成绩\t思政成绩\tPython成绩")
for student in students:
    print("\t".join(map(str,student)))
英语=sum([student[4]for student in students])/len(students)
政治=sum([student[5]for student in students])/len(students)
py=sum([student[6]for student in students])/len(students)
print(f"\n英语的平均成绩: {英语:.1f}")
print(f"政治的平均成绩: {政治:.1f}")
print(f"Python的平均成绩: {py:.1f}")
