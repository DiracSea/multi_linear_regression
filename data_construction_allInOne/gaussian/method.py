import numpy as np
from data_construction_allInOne.gaussian import timeNorm as tn
from data_construction_allInOne.gaussian import dataTrait as dataT

# 对规划院规律的降雨量进行编码
def encode(tuple_curP,tuple_oneP,tuple_thrP):
    cur_P=tuple_curP
    one_P=tuple_oneP
    thr_P=tuple_thrP
    startT=min(thr_P[0])
    endT=max(thr_P[1])
    
    #根据降雨始末时间与数据个数，生成对应大小的矩阵
    cur_num=len(cur_P[0])
    m=3*cur_num#行数
    n=tn.tens(startT,endT)+1#10间隔数，即列数
    precipMat=np.zeros((m,n))
    precipMat=precipMat.astype('float32')

    for i in range(0,cur_num):
        #处理curP所对应的行数，起始列，终止列:
        cur_Row=3*i+0
        cur_SCol=tn.tens(startT,cur_P[0][i])
        cur_ECol=tn.tens(startT,cur_P[1][i])
        cur_Precip=cur_P[2][i]
        #处理oneP所对应的行数，起始列，终止列:
        one_Row=3*i+1
        one_SCol=tn.tens(startT,one_P[0][i])
        one_ECol=tn.tens(startT,one_P[1][i])
        one_Precip=one_P[2][i]
        #处理thrP所对应的行数，起始列，终止列:
        thr_Row=3*i+2
        thr_SCol=tn.tens(startT,thr_P[0][i])
        thr_ECol=tn.tens(startT,thr_P[1][i])
        thr_Precip=thr_P[2][i]
        #填充1，因为使用的为间隔，以起始列为基准，终止列没有对应的时间段
        precipMat[cur_Row,cur_SCol:(cur_ECol)]=1
        precipMat[one_Row,one_SCol:(one_ECol)]=1
        precipMat[thr_Row,thr_SCol:(thr_ECol)]=1
        #填充降雨量数据
        try:
            precipMat[cur_Row,-1]=cur_Precip
        except ValueError as e:
            print("%scur_Precip is %s"%(e,cur_Precip ))
        try:
            precipMat[one_Row,-1]=one_Precip
        except ValueError as e:
            print("%sone_Precip is %s"%(e,one_Precip ))
        try:
            precipMat[thr_Row,-1]=thr_Precip
        except ValueError as e:
            print("%sthr_Precip is %s"%(e,thr_Precip ))
        
    #补全一场雨间，数据缺失的情况，即一些x的系数在第个方程中均为0的情况
    checkPara=precipMat[:,:-1].sum(axis=0)
    loc_noPara=np.argwhere(checkPara==0)
    for i in loc_noPara:
        addArray=np.zeros((1,n))
        addArray[0,i[0]]=1
        precipMat=np.row_stack((precipMat,addArray))
    
    #条件信息：降雨量为0对应的方程中的未知数，其结果都为0
    count=1
    for row in precipMat:
        if count==1:
            matrix=dataT.findZeroX(row)
            count=0
        else:
            matrix=np.row_stack((matrix,dataT.findZeroX(row)))
    precipMat=matrix.getA()

    return startT,endT,precipMat

#将矩阵根据降雨量开始时间解码为时间雨量数据，类型为list
def decode(startT,matrix):
    #检查参数子矩阵，是否每行都只有一个10分钟的时间段
    paraMatrix=matrix[:,:-1]
    paraMatrix=paraMatrix.astype('int32')#parameter矩阵只由整数组成
    absMatrix=abs(paraMatrix)
    rowSum=absMatrix.sum(axis=1)
    m=1+np.argwhere(rowSum!=0)[-1,0]#m为系数非0的个数
    judgeArray=np.zeros(m)
    judgeArray=judgeArray.astype('int32')
    for i in range(m):
        if rowSum[i] == 1:
            judgeArray[i]=1
        else:
            judgeArray[i]=-1

    strSeries=[]
    rows=len(judgeArray)
    for i in range(rows):
        curRow=matrix[i,:-1]
        startCol=np.argwhere(curRow==1)[0,0]
        endCol=np.argwhere(curRow!=0)[-1,0]
        paras=curRow[startCol:endCol+1]#去头去尾留中间
        numOfPara=len(paras)
        
        timeIntS=tn.tensLater(startT,startCol)
        timeIntE=tn.tensLater(timeIntS,numOfPara)
        precip=round(matrix[i,-1],1)#高斯消元处理后的降雨量数据,理应为小数点后一位
        #strRow的默认值,默认该行数据为可分情况
        strRow=[tn.getStrTime(timeIntS),tn.getStrTime(timeIntE),precip]
        if np.size(np.argwhere(paras!=1)) != 0:#完全不可细分情况
            strRow[2]='It\'s a trap!'
            strSeries.append([strRow[0],strRow[1],strRow[2]])#与下面代码中的list格式相对应
        elif numOfPara == 1:
            strSeries.append([strRow[0],strRow[1],strRow[2]])
        else:#不能使用gaussian细分的情况
            exTimeSeries=dataT.divPrecip(timeIntS,timeIntE,precip)
            if precip == 0:#若降雨量为零，则不需要插值
                strRow[2]=0
                for j in range(numOfPara):
                    strRow[0]=tn.getStrTime(exTimeSeries[j][0])
                    strRow[1]=tn.getStrTime(exTimeSeries[j][1])
                    strSeries.append([strRow[0],strRow[1],strRow[2]])#防止list的变化性质导致出的bug
            else:#降雨量不为零，需要用到插值法
                for j in range(numOfPara):
                    strRow[0]=tn.getStrTime(exTimeSeries[j][0])
                    strRow[1]=tn.getStrTime(exTimeSeries[j][1])
                    strRow[2]=exTimeSeries[j][2]
                    strSeries.append([strRow[0],strRow[1],strRow[2]])
    
    return strSeries

def block(startT,endT,amount):

    #根据降雨量数值进行粗选
    m=len(amount)
    start=0
    end=m-1

    checkList=[]
    for i in range(m):
        if amount[i]==0:
            start=i
        else:
            end=i
            if i==m-1:
                checkList.append([start,end])
            elif amount[i+1]==0:
                checkList.append([start,end])
    
    #根据三小时降雨的起始时间进行细分
    n=len(checkList)
    start=checkList[0][0]
    end=checkList[0][1]

    newList=[]
    for i in range(n-1):
        index1=checkList[i][0]
        index2=checkList[i][1]
        index3=checkList[i+1][0]
        index4=checkList[i+1][1]

        if startT[index3]<endT[index2]:
            end=index4
        else:
            newList.append([start,end])
            start=index3
            end=index4
        
    newList.append([start,end])

    return newList