import os

# 1. 成绩录入函数
def input_scores(num_students: int) -> list[float]:
    """
    功能：根据输入的学生数量，依次录入每位学生的成绩，确保成绩合法。
    参数：
        num_students (int): 待录入学生的数量。
    返回值：
        list[float]: 有效的成绩列表。
    异常处理：
        - 若输入非数值类型，提示“输入的不是有效数值，请重新输入！”
        - 若成绩超出0-100范围，提示“成绩必须在0到100之间，请重新输入！”
    """
    scores = []
    for i in range(num_students):
        while True:
            try:
                score = float(input(f"请输入第{i + 1}位学生的成绩（0-100）："))
                if score < 0 or score > 100:
                    print("成绩必须在0到100之间，请重新输入！")
                else:
                    scores.append(score)
                    break
            except ValueError:
                print("输入的不是有效数值，请重新输入！")
    return scores

# 2. 平均分计算函数
def calculate_average(scores: list[float]) -> float:
    """
    功能：计算成绩列表的平均分，若列表为空则返回0.0。
    参数：
        scores (list[float]): 学生成绩列表。
    返回值：
        float: 平均分，保留2位小数。
    """
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 2)

# 3. 成绩等级评定函数
def grade_score(score: float) -> str:
    """
    功能：根据成绩评定等级。
    参数：
        score (float): 学生成绩。
    返回值：
        str: 对应的成绩等级。
    等级划分规则：
        - 90及以上为“优秀”
        - 80-89为“良好”
        - 70-79为“中等”
        - 60-69为“及格”
        - 60以下为“不及格”
    """
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 70:
        return "中等"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"

# 4. 结果保存函数
def save_results(scores: list[float], file_path: str = "score_result.txt") -> None:
    """
    功能：将成绩列表、平均分、成绩等级分布写入指定文件。
    参数：
        scores (list[float]): 学生成绩列表。
        file_path (str, 可选): 保存文件的路径，默认值为“score_result.txt”。
    返回值：
        None
    异常处理：
        - 若保存过程中出现错误，提示“保存文件时出错：XXX”
    文件内容要求：
        - 学生成绩列表：[成绩1, 成绩2, ...]
        - 全体学生的平均分：XX.XX
        - 成绩等级分布：优秀X人、良好X人、中等X人、及格X人、不及格X人
    """
    try:
        with open(file_path, 'w') as f:
            avg = calculate_average(scores)
            grade_counts = {"优秀": 0, "良好": 0, "中等": 0, "及格": 0, "不及格": 0}

            for score in scores:
                grade = grade_score(score)
                grade_counts[grade] += 1

            f.write(f"学生成绩列表：{scores}\n")
            f.write(f"全体学生的平均分：{avg}\n")
            f.write(f"成绩等级分布：")
            f.write(f"优秀{grade_counts['优秀']}人、")
            f.write(f"良好{grade_counts['良好']}人、")
            f.write(f"中等{grade_counts['中等']}人、")
            f.write(f"及格{grade_counts['及格']}人、")
            f.write(f"不及格{grade_counts['不及格']}人\n")
        print(f"结果已保存至：{file_path}")
    except Exception as e:
        print(f"保存文件时出错：{e}")

# 5. 主函数
def main() -> None:
    """
    主函数，展示功能菜单，接收用户输入的功能编号，调用对应函数完成功能。
    """
    scores = []  # 用于存储学生成绩
    while True:
        print("\n===== 学生成绩分析系统 =====")
        print("功能入口：")
        print("1-录入成绩")
        print("2-计算平均分")
        print("3-评定单成绩等级")
        print("4-保存结果")
        print("0-退出")

        choice = input("请输入功能编号：")
        
        # 录入成绩
        if choice == "1":
            while True:
                try:
                    num_students = int(input("请输入要录入的学生数量："))
                    if num_students <= 0:
                        print("请输入正整数！")
                    else:
                        break
                except ValueError:
                    print("请输入有效的数字！")
            scores = input_scores(num_students)

        # 计算平均分
        elif choice == "2":
            if not scores:
                print("请先录入成绩！")
            else:
                avg = calculate_average(scores)
                print(f"全体学生的平均分：{avg}")

        # 评定单成绩等级
        elif choice == "3":
            while True:
                try:
                    score = float(input("请输入要评定的成绩："))
                    if 0 <= score <= 100:
                        break
                    else:
                        print("成绩必须在0到100之间，请重新输入！")
                except ValueError:
                    print("输入的不是有效数值，请重新输入！")
            grade = grade_score(score)
            print(f"成绩{score}的等级：{grade}")

        # 保存结果
        elif choice == "4":
            if not scores:
                print("请先录入成绩！")
            else:
                save_results(scores)

        # 退出
        elif choice == "0":
            print("程序结束！")
            break

        # 非法输入
        else:
            print("无效的功能编号，请输入0-4之间的数字！")

if __name__ == "__main__":
    main()
