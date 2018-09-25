import datetime as dt

#时间方法

#将tuple格式的时间数据转换成好看的字符串格式
def tuple2str(tuple_time):
    time=dt.datetime(*tuple_time)
    return time.strftime("%Y/%m/%d %H:%M:%S") 

#将datetime格式的时间数据转换成tuple格式
def time2tuple(time):
    return (time.timetuple().tm_year, time.timetuple().tm_mon, time.timetuple().tm_mday, time.timetuple().tm_hour, time.timetuple().tm_min,time.timetuple().tm_sec)

#判断两个时间中有多少个整分钟
def ones(time1,time2):
    startT=min(time1,time2)
    endT=max(time1,time2)
    delta=endT-startT

    return round(delta.total_seconds()/60)

#已知起始与结束时间，生成一段间隔为1分钟的时间序列
def tupleSeries(tuple_time1,tuple_time2):
    time1=dt.datetime(*tuple_time1)
    time2=dt.datetime(*tuple_time2)
    if time1>time2:
        return []
    else:
        length=ones(time1,time2)
        return [time2tuple(time1+i*dt.timedelta(minutes=1)) for i in range(length+1)]

#时间2到时间1间，相差的秒数
def diffOfTuple(tuple_time1,tuple_time2):
    return (dt.datetime(*tuple_time2)-dt.datetime(*tuple_time1)).total_seconds()

    return sortedData[0],sortedData[1]