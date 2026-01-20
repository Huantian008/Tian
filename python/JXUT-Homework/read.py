# 读取文件并解析数据
with open('scores.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

students = []
for line in lines:
    data = line.strip().split(',')
    student = {
        '学号': data[0],
        '姓名': data[1],
        '语文': int(data[2]),
        '数学': int(data[3]),
        '英语': int(data[4])
    }
    students.append(student)

print(students)

failed_students = []
max_scores = {'语文': 0, '数学': 0, '英语': 0}
min_scores = {'语文': 100, '数学': 100, '英语': 100}
total_scores = {'语文': 0, '数学': 0, '英语': 0}
total_students = len(students)

# 计算总分、平均分，并找出各科目的最高分、最低分
for student in students:
    total_score = student['语文'] + student['数学'] + student['英语']
    average_score = total_score / 3
    student['总分'] = total_score
    student['平均分'] = average_score

    for subject in ['语文', '数学', '英语']:
        total_scores[subject] += student[subject]
        max_scores[subject] = max(max_scores[subject], student[subject])
        min_scores[subject] = min(min_scores[subject], student[subject])

    # 筛选出不及格的学生
    if student['语文'] < 60 or student['数学'] < 60 or student['英语'] < 60:
        failed_students.append(student)

# 计算各科目的平均分
avg_scores = {subject: total_scores[subject] / total_students for subject in total_scores}

print(f"各科目最高分：{max_scores}")
print(f"各科目最低分：{min_scores}")
print(f"各科目平均分：{avg_scores}")
print(f"不及格学生：{failed_students}")

# 按总分降序排序
students_sorted = sorted(students, key=lambda x: x['总分'], reverse=True)

# 写入分析结果
with open('scores_analysis.txt', 'w', encoding='utf-8') as file:
    file.write("学号, 姓名, 语文, 数学, 英语, 总分, 平均分\n")
    for student in students_sorted:
        file.write(f"{student['学号']}, {student['姓名']}, {student['语文']}, {student['数学']}, {student['英语']}, {student['总分']}, {student['平均分']}\n")

# 将不及格学生信息写入failed_students.txt
with open('failed_students.txt', 'w', encoding='utf-8') as file:
    for student in failed_students:
        file.write(f"{student['学号']}, {student['姓名']}, {student['语文']}, {student['数学']}, {student['英语']}\n")
