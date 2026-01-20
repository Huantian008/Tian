import math

# 获取直角三角形两条直角边的长度
a = float(input("请输入直角三角形的第一条直角边长度: "))
b = float(input("请输入直角三角形的第二条直角边长度: "))

# 计算斜边 c 的长度
c = math.sqrt(a**2 + b**2)

# 计算面积
area = (a * b) / 2

# 计算周长
perimeter = a + b + c

# 输出计算结果
print(f"斜边的长度为: {c:.2f}")
print(f"面积为: {area:.2f}")
print(f"周长为: {perimeter:.2f}")
