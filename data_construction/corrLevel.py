import csv
import datetime
from .timeNorm import fives
from data_construction.tmp.cfg import read_WDRS

rain_sensor=[["1048","8267"],
             ["1023","7527"],
             ["1024","4410"],
             ["1033","5272"],
             ["1027","1560"],
             ["1070","6511"],
             ["1070","7170"],
             ["1077","0893"],
             ["10701","2"],
             ["10701","9"],
             ["10701","20"]]

def corrRain(sensorCode):
    rainCode=-1
    for i in rain_sensor:
        if i[1]==sensorCode:
            rainCode=i[0]
    if rainCode==-1:
        print("No such rain station to sensor %s" %sensorCode)

    return rainCode

#根据水位、降雨两列数据的起点时间,水位的mod(0~4间的整数)，找到与降雨对应的index
def rain_corrLine(level_startT,rain_startT,rain_index,mod):
    noModTime=level_startT-datetime.timedelta(minutes=mod)#先把水位拉回到原本的5分钟位置
    numOfFive=fives(rain_startT,noModTime)
    
    rainTime=rain_startT+rain_index*datetime.timedelta(minutes=10)
    if rainTime<level_startT:#判断是否存在对应降雨的水位数据
        level_index=-1
    else:
        level_index=2*rain_index-numOfFive
    return level_index

#根据水位两列数据的起点时间,水位的mod(0~4间的整数)，找到与降雨对应的index
def level_corrLine(level_startT1,level_startT2,level_index1,mod1,mod2):
    noModTime1=level_startT1-datetime.timedelta(minutes=mod1)#先把水位拉回到原本的5分钟位置
    noModTime2=level_startT2-datetime.timedelta(minutes=mod2)#先把水位拉回到原本的5分钟位置
    numOfFive=fives(noModTime1,noModTime2)

    levelTime1=level_startT1+level_index1*datetime.timedelta(minutes=5)
    if levelTime1<level_startT2:#判断是否存在对应降雨的水位数据
        level_index2=-1
    else:
        level_index2=level_index1-numOfFive
    return level_index2