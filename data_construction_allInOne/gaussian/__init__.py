import datetime
import numpy as np

from data_construction_allInOne.gaussian.dataTrait import findZeroX, zeroPreInfo
from data_construction_allInOne.gaussian.timeNorm import getTime, getStrTime
from data_construction_allInOne.gaussian.gaussian import gaussianElimination
from data_construction_allInOne.gaussian.method import encode, decode, block

# 排序,拆块,编码,消元,解码,填充
def solve_rainfall(*data_listMatrix):
    '''
    param:{cur_start_t,cur_ter_t,rainfall,one_hr_start_t,one_hr_ter_t,one_hr_rainfall,three_hrs_start_t,three_hrs_ter_t,three_hrs_rainfall}
    '''
    # 排序
    sorted_listMatrix=sorted(data_listMatrix,key=lambda x:x[7])
    startTforAll=sorted_listMatrix[0][6]
    endTforAll=sorted_listMatrix[-1][7]
    # 拆块
    invData=list(map(list,zip(*sorted_listMatrix)))
    checkBlock=block(invData[6],invData[7],invData[8])

    allData=[]
    for eachBlock in checkBlock:
        # 编码
        start=eachBlock[0]
        end=eachBlock[1]
        tuple_curP=(invData[0][start:end+1],invData[1][start:end+1],invData[2][start:end+1])
        tuple_oneP=(invData[3][start:end+1],invData[4][start:end+1],invData[5][start:end+1])
        tuple_thrP=(invData[6][start:end+1],invData[7][start:end+1],invData[8][start:end+1])
        startT, endT, array_matrix=encode(tuple_curP,tuple_oneP,tuple_thrP)
        # 消元
        gau=gaussianElimination(array_matrix,"Y")
        # 解码
        list_str_rainfall=decode(startT,gau)
        # 填充
        list_str_zero=zeroPreInfo(startTforAll,startT)
        allData=allData+list_str_zero
        startTforAll=endT
        allData=allData+list_str_rainfall

    list_str_zero=zeroPreInfo(startTforAll,endTforAll)
    allData=allData+list_str_zero

    return allData