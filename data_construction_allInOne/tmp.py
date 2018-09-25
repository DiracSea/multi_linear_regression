import os
import csv
from data_construction_allInOne.timeNorm import getFileTime
from data_construction_allInOne.interpolation import interpolation
from data_construction_allInOne.gaussian import solve_rainfall
from data_construction_allInOne.error import EmptyRainfallError, EmptyWaterlevelError, NoMethodError

curr_path=(os.path.split(__file__))[0]
TMP_DIR = os.path.join(curr_path,"tmp")

def norm_waterlevel(origin_wl,deviceID,mod):
    if origin_wl==[]:
        raise EmptyWaterlevelError("The data got from waterlevel device-%s is empty."%str(deviceID))

    invData=list(map(list,zip(*origin_wl)))
    time_list=invData[0]
    startT=min(time_list)
    endT=max(time_list)

    dirName=os.path.join(TMP_DIR,"level-"+str(mod))
    fileName=str(deviceID)+'-'+getFileTime(startT)+'-'+getFileTime(endT)+'.csv'

    path=os.path.join(dirName,fileName)
    if os.path.exists(path):
        solveData=[]
        csv_file=csv.reader(open(path,'r'))
        for row in csv_file:
            solveData.append(row)
    else:
        solveData=interpolation(mod,origin_wl)
        m=len(solveData)
        n=len(solveData[0])
        with open(path,'w') as f:
            for j in range(m):
                for k in range(n-1):
                    f.write(str(solveData[j][k])+',')
                f.write(str(solveData[j][n-1]))
                f.write('\n')

    return solveData

def norm_rainfall(origin_rf,stationID,sort):
    if origin_rf==[]:
        raise EmptyRainfallError("The data got from rainfall station-%s is empty."%str(stationID))

    invData=list(map(list,zip(*origin_rf)))
    startT=min(invData[6])
    endT=max(invData[7])

    if int(sort)==0:
        dirName=os.path.join(TMP_DIR,"rain-10")
        fileName=str(stationID)+'-'+getFileTime(startT)+'-'+getFileTime(endT)+'.csv'

        path=os.path.join(dirName,fileName)
        if os.path.exists(path):
            solveData=[]
            csv_file=csv.reader(open(path,'r'))
            for row in csv_file:
                solveData.append(row)
        else:
            solveData=solve_rainfall(*origin_rf)
            m=len(solveData)
            n=len(solveData[0])
            with open(path,'w') as f:
                for j in range(m):
                    for k in range(n-1):
                        f.write(str(solveData[j][k])+',')
                    f.write(str(solveData[j][n-1]))
                    f.write('\n')
    else:
        raise NoMethodError("由于没有对应的非规划院数据集，处理非规划院数据集算法并未编写。")

    return solveData