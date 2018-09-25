from data_construction_allInOne.gaussian import timeNorm as tn
import numpy as np

#平均插值————平分不能细分的降雨量，并返回相应的时间段
def divPrecip(time1,time2,precip):
    num=tn.tens(time1,time2)
    perPrecip=round(precip/num,3)
    timeList=tn.series(time1,time2)

    return [[timeList[i],timeList[i+1],perPrecip] for i in range(num)]

#条件信息1：由于x>0，则降雨量为零对应的方程式中的未知数都为0。输入对应行的向量（非零元素均为1），输出对应的方程矩阵。
def findZeroX(array):
    matrix=np.mat(array)
    if matrix[0,-1]==0:
        one_loc=np.argwhere(matrix==1)
        m=len(one_loc)
        n=matrix.shape[1]
        matrix=np.zeros((m,n))
        for i in range(m):
            matrix[i,one_loc[i,1]]=1
    return matrix
    
#条件信息2：未知的降雨量数据均为0。输入开始时间与结束时间，输出对应格式的降雨信息。
def zeroPreInfo(timeStart,timeEnd):
    precipInfo=[]
    if timeStart < timeEnd:
        series=tn.series(timeStart,timeEnd)
        for i in range(len(series)-1):
            precipInfo.append([tn.getStrTime(series[i]),tn.getStrTime(series[i+1]),0])
    return precipInfo