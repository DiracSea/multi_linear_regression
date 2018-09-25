from data_construction_allInOne.interpolation import timeNorm as tn
from data_construction_allInOne.interpolation.method import linear

import datetime as dt
import xlrd
import os
from os.path import splitext

def interpolation(mod,data_listMatrix):

    #提取数据
    postData=[]#初始化处理后的数据List

    data_sorted=sorted(data_listMatrix)
    m=len(data_sorted)
    for i in range(m-1):
        #确定每一个区间的起、终时间，与对应的值
        startT=data_sorted[i][0]
        endT=data_sorted[i+1][0]
        startValue=data_sorted[i][1]
        endValue=data_sorted[i+1][1]

        #先将其转换成tuple格式,再分别“舍入”
        tuple_startT=tn.time2tuple(startT)
        tuple_endT=tn.time2tuple(endT)
        
        #区间下界的秒设为0，并在下一行加一分钟
        divstartT=tuple_startT[:-2]+(tuple_startT[-2],0)
        #这里使用时间格式来进行加一分钟的处理，来避免bug
        divstartT=tn.time2tuple(dt.datetime(*divstartT)+dt.timedelta(minutes=1))
        divendT=tuple_endT[:-1]+(0,)#区间上界秒设为0
        #生成对应区间间隔一分钟的时间序列
        series=tn.tupleSeries(divstartT,divendT)

        for k in series:
            if k[4]%5==mod:#判断序列中哪几个是符合要求的
                #以起始时间为x零点，开始进行线性插值
                x1=0
                x2=tn.diffOfTuple(tuple_startT,tuple_endT)
                x=tn.diffOfTuple(tuple_startT,k)
                interValue=linear(x,x1,x2,startValue,endValue)
                if x2 >=600:#若对应区间时长大于10分钟，则水位估计无意义
                    interValue=-1
                postData.append([tn.tuple2str(k),interValue])#将数据输入到之前准备好的List中
    
    return postData