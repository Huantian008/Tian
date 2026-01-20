import math
def triangle_area(a,b,c):
    if a <=0 or b<=0 or c<0:
        return None
    if a+b<=c or a+c<=b or b+c<=a:
        return None
    s=(a+b+c)/2
    area =math.sqrt(s*(s-a)*(s-b)*(s-c))
    return round(area,3)
print(triangle_area(3, 4, 5)) 
