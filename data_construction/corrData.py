from .corrLevel import corrRain, rain_corrLine, level_corrLine
from .timeNorm import getTime
import csv
from .rainfallInterval import rainfallInterval
import os
#生成间隔一定的降雨-水位对应数据。例：
#sensorcode=1560,4410,5272,7170#已有哪些井盖数据
#diff=1#生成时间上相关多久的两列数据，对应的时刻上，水位迟于降雨量
def rain_level_Data(sensorcode, diff): 
    raincode = corrRain(sensorcode)
    numOfFive = diff//5
    mod = diff % 5

    rainFile = str(raincode)+'.csv'
    levelFile = '.\\data_construction\\inputWaterLevel\\mod'+str(mod)+'\\sensor_'+sensorcode+'.csv'

    #获取降雨与水位数据
    (intList, rainData) = rainfallInterval(rainFile)
    levelData = []
    csv_file = csv.reader(open(levelFile, 'r'))
    for j in csv_file:
        levelData.append(j)

    inteData = []
    rain_startT = getTime(rainData[0][1])  # 降雨的第一个区间的结束时间
    level_startT = getTime(levelData[0][0])  # 水位的第一个时间点
    level_endIndex = len(levelData)-1
    numOfRainfall=0
    for j in intList:
        ifHaveAdd=0#初始化，还没加上1
        for k in range(j[0], j[1]+1):
            level_index = rain_corrLine(level_startT, rain_startT, k, mod)
            if (level_index != -1) & (level_index+numOfFive <= level_endIndex):
                if ifHaveAdd==0:
                    numOfRainfall=numOfRainfall+1#还没加1，来，把1加上
                    ifHaveAdd=1#好吧，已经加上了
                level_index = level_index+numOfFive
                inteData.append([numOfRainfall]+[k]+[level_index])
                #inteData.append(rainData[k]+levelData[level_index])
    
    return (rainData,levelData,inteData)

#在mod1的基准下，生成与之对应的，各行时间差相同的平行数据列
def level_level_Data(sensorcode,mod1,diff):
    numOfFive=(diff+mod1)//5
    mod2=(diff+mod1)%5

    levelData1=[]
    levelData2=[]
    levelFile1 = '.\\inputWaterLevel\\mod'+str(mod1)+'\\sensor_'+sensorcode+'.csv'
    levelFile2 = '.\\inputWaterLevel\\mod'+str(mod2)+'\\sensor_'+sensorcode+'.csv'
    csv_file1 = csv.reader(open(levelFile1, 'r'))
    for j in csv_file1:
        levelData1.append(j)
    csv_file2 = csv.reader(open(levelFile2, 'r'))
    for j in csv_file2:
        levelData2.append(j)

    inteData=[]
    level_StartT1=getTime(levelData1[0][0])
    level_StartT2=getTime(levelData2[0][0])
    level_endIndex2=len(levelData2)-1
    for j in range(len(levelData1)):
        level_Index2=level_corrLine(level_StartT1,level_StartT2,j,mod1,mod2)
        if (level_Index2+numOfFive<=level_endIndex2) & (level_Index2!=-1):
            level_Index2=level_Index2+numOfFive
            inteData.append(levelData1[j]+levelData2[level_Index2])

    return (levelData1,levelData2,inteData)

def rain_level_AllData(sensorcode, diff): 
    raincode = corrRain(sensorcode)
    numOfFive = diff//5
    mod = diff % 5

    rainFile = str(raincode)+'.csv'
    my_path = os.path.abspath(os.path.dirname(__file__))
    levelFile = os.path.join(my_path,'inputWaterLevel\\mod'+str(mod)+'\\sensor_'+sensorcode+'.csv')

    #获取降雨与水位数据
    tmp, rainData = rainfallInterval(rainFile)
    levelData = []
    csv_file = csv.reader(open(levelFile, 'r'))
    for j in csv_file:
        levelData.append(j)

    dataInfo = []
    rain_startT = getTime(rainData[0][1])  # 降雨的第一个区间的结束时间
    level_startT = getTime(levelData[0][0])  # 水位的第一个时间点
    level_endIndex = len(levelData)-1
    for j in range(len(rainData)):
        level_index = rain_corrLine(level_startT, rain_startT, j, mod)
        if (level_index != -1) & (level_index+numOfFive <= level_endIndex):
            level_index = level_index+numOfFive
            dataInfo.append([j]+[level_index]+[level_index-2*j])
            break

    return (rainData,levelData,dataInfo)

    # outputName='.\\data_construction\\test.csv'
    # m = len(dataInfo)
    # n = len(dataInfo[0]) #因为存在标签，所以这里直接给明需要的数据列数
    # with open(outputName, 'w') as f:
    #     for j in range(m):
    #         for k in range(n-1):
    #             f.write(str(dataInfo[j][k])+',')
    #         f.write(str(dataInfo[j][n-1]))
    #         f.write('\n')