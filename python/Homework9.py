def chengji(score):
    if score < 0 or score > 100:
        return "无意义"

    if 90 <= score <= 100:
        return "优"

    elif 80 <= score < 90:
        return "良"

    elif 70 <= score < 80:
        return "中"

    elif 60 <= score < 70:
        return "及格"

    else:
        return "不及格"
print(chengji(95))
print(chengji(83))
print(chengji(75))
print(chengji(63))
print(chengji(40))
print(chengji(-5))
