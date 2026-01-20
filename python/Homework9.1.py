def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def mul(a,b):
    return a*b
def div(a,b):
    if b==0:
        return "错误：除数不能为0"
    return a/b
def mod(a,b):
    if b==0:
        return"错误：除数不能为0"
    return a%b
def calculator(a,b,op):
    if op == '+':
        return add(a, b)
    elif op == '-':
        return sub(a, b)
    elif op == '*':
        return mul(a, b)
    elif op == '/':
        return div(a, b)
    elif op == '%':
        return mod(a, b)
    else:
        return "错误：不支持的运算符"
# 测试
print(calculator(10, 5, '+'))  
print(calculator(10, 5, '-'))  
print(calculator(10, 5, '*'))  
print(calculator(10, 5, '/')) 
print(calculator(10, 3, '%'))