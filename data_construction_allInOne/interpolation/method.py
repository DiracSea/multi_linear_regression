#线性插值法
def linear(x,x1,x2,y1,y2):
    if x2-x1==0:
        result=y1
    else:
        result=y1+(x-x1)*(y2-y1)/(x2-x1)
    return result