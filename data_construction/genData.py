from .corrData import rain_level_Data, level_level_Data, rain_level_AllData
import os

#生成数据:输入：降雨量为X，水位为Y；输出：水位Y，后面的数字代表preTime。
###参数###
# numOfX=5
# numOfY=2
# preTime=1108#提前几分钟预测，10为提前10分钟
###参数###

def genData(numOfX,numOfY,preTime,sensorcode):

    dataSet=[]
    (rainData,levelData_pre,data_Pt_YtPreTime)=rain_level_Data(sensorcode,preTime)
    (rainData,levelData_now,data_Pt_YtNow)=rain_level_Data(sensorcode,0)
    
    #有一个隐性的bug，但在数据集里未出现。这里写上了检验出现Bug的if语句。
    m=len(data_Pt_YtNow)
    n=len(data_Pt_YtPreTime)
    rainInd1=data_Pt_YtNow[0][1]
    rainInd2=data_Pt_YtPreTime[0][1]
    if (m!=n) | (rainInd1!=rainInd2):
        #若在新数据集上出现了预期的bug，则提示。
        print("There exists a programming bug. Come and fix it!")
    else:
        #开始分配index及其对应的数据集
        for j in range(n):
            ifMinusExist=0#用于判断是否有水位数据为负一
            line_Pre=data_Pt_YtPreTime[j]
            line_Now=data_Pt_YtNow[j]

            whichRain=line_Pre[0]             
            rain_Ind=line_Pre[1]     
            levelnow_Ind=line_Now[2]                   
            levelpre_Ind=line_Pre[2]

            dataLine=(whichRain,)
            for k in range(numOfX):
                dataLine=dataLine+(rainData[rain_Ind-k][2],)
            for k in range(numOfY):
                dataLine=dataLine+(levelData_now[levelnow_Ind-k][1],)
            dataLine=dataLine+(levelData_pre[levelpre_Ind][1],)

            #存在插值为无效的水位点，即值为-1，这里要判断一下
            for k in dataLine:
                if float(k)==-1:
                    ifMinusExist=1
                    #print("There exists one line that has -1.")
            if ifMinusExist==0:
                dataSet.append(list(map(float,dataLine)))

        return dataSet

def genData_AllTime(numOfX,numOfY,preTime,sensorcode):

    dataSet=[]
    (rainData,levelData_pre,dataInfo_PreTime)=rain_level_AllData(sensorcode,preTime)
    (rainData,levelData_now,dataInfo_Now)=rain_level_AllData(sensorcode,0)

    rainInd1=dataInfo_PreTime[0][0]
    rainInd2=dataInfo_Now[0][0]
    b1=dataInfo_PreTime[0][2]
    b2=dataInfo_Now[0][2]
    rainIndBase=max(rainInd1,rainInd2)

    for i in range(rainIndBase,len(rainData)+1):
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
                dataLine=dataLine+(levelData_now[levelIndex_Now-j][1],)
            dataLine=dataLine+(levelData_pre[levelIndex_PreTime][1],)
    
            #存在插值为无效的水位点，即值为-1，这里要判断一下
            for k in dataLine:
                if float(k)==-1:
                    ifMinusExist=1
            if ifMinusExist==0:
                dataSet.append(list(map(float,dataLine)))

    return dataSet