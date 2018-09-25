import datetime

#1、处理字符串格式：
#变为时间格式
def getTime(strTime):
    t=datetime.datetime.strptime(strTime,'%Y\%m\%d %H:%M:%S')
    
    return t

#2、处理时间格式
#生成对应格式的字符串时间
def getStrTime(time):
    return time.strftime("%Y/%m/%d %H:%M:%S") 

#有多少个10分钟
def tens(time1,time2):
    startT=min(time1,time2)
    endT=max(time1,time2)
    delta=endT-startT

    return round(delta.total_seconds()/600)
#返回n个10分钟段后的时间点
def tensLater(time,n):
    return time+n*datetime.timedelta(minutes=10)
#生成时间序列，包括最后一个时间点
def series(time1,time2):
    length=tens(time1,time2)
    startT=min(time1,time2)

    return [startT+i*datetime.timedelta(minutes=10) for i in range(length+1)]