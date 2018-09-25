import csv
from data_construction_allInOne.timeNorm import getTime, fives
import datetime

def genData_rain10(numOfX,numOfY,rainData,levelData_pre,levelData_now,preTime):

    dataSet=[]
    dataInfo_PreTime=rain10_level(rainData,levelData_pre,preTime)
    dataInfo_Now=rain10_level(rainData,levelData_now,0)

    rainInd1=dataInfo_PreTime[0][0]
    rainInd2=dataInfo_Now[0][0]
    b1=dataInfo_PreTime[0][2]
    b2=dataInfo_Now[0][2]
    rainIndBase=max(rainInd1,rainInd2)

    for i in range(rainIndBase,len(rainData)):
        levelIndex_PreTime=2*i+b1
        levelIndex_Now=2*i+b2
        maxIndex_PreTime=len(levelData_pre)-1
        maxIndex_Now=len(levelData_now)-1

        ifMinusExist=0
        dataLine=()
        if (i-numOfX>=-1) & (levelIndex_Now-2*(numOfY-1)>=0) & (levelIndex_PreTime<=maxIndex_PreTime) & (levelIndex_Now<=maxIndex_Now):
            for j in range(numOfX):
                dataLine=dataLine+(rainData[i-j][2],)
            for j in range(numOfY):
                dataLine=dataLine+(levelData_now[levelIndex_Now-2*j][1],)
            dataLine=dataLine+(levelData_pre[levelIndex_PreTime][1],)
    
            #存在插值为无效的水位点，即值为-1，这里要判断一下
            for k in dataLine:
                if float(k)==-1:
                    ifMinusExist=1
            if ifMinusExist==0:
                dataSet.append(list(map(float,dataLine)))

    return dataSet

def rain10_level(rainData, levelData, diff): 
    numOfFive = diff//5
    mod = diff % 5

    dataInfo = []
    rain_startT = getTime(rainData[0][1])  # 降雨的第一个区间的结束时间
    level_startT = getTime(levelData[0][0])  # 水位的第一个时间点
    level_endIndex = len(levelData)-1
    for j in range(len(rainData)):
        level_index = rain10_line(level_startT, rain_startT, j, mod)
        if (level_index != -1) & (level_index+numOfFive <= level_endIndex):
            level_index = level_index+numOfFive
            dataInfo.append([j]+[level_index]+[level_index-2*j])
            break

    return dataInfo

#根据水位、降雨两列数据的起点时间,水位的mod(0~4间的整数)，找到与降雨对应的index
def rain10_line(level_startT,rain_startT,rain_index,mod):
    noModTime=level_startT-datetime.timedelta(minutes=mod)#先把水位拉回到原本的5分钟位置
    numOfFive=fives(rain_startT,noModTime)
    
    rainTime=rain_startT+rain_index*datetime.timedelta(minutes=10)
    if rainTime<level_startT:#判断是否存在对应降雨的水位数据
        level_index=-1
    else:
        level_index=2*rain_index-numOfFive
    return level_index