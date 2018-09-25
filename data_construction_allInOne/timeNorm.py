import datetime

#1、处理字符串格式：
#变为时间格式
def getTime(strTime):
    t=datetime.datetime.strptime(strTime,'%Y/%m/%d %H:%M:%S')
    
    return t

#2、处理时间格式
#生成对应格式的字符串时间
def getFileTime(time):
    return time.strftime("%Y%m%d%H%M%S") 

#有多少个5分钟
def fives(startT,endT):
    delta=endT-startT
    return round(delta.total_seconds()/300)