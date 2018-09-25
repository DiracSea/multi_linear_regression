from data_construction_allInOne.vonorio.data import get_waterlevel, get_rainfall
from data_construction_allInOne.vonorio.cfg import read_WDRS
from data_construction_allInOne.tmp import norm_waterlevel, norm_rainfall
from data_construction_allInOne.corrData import rain10_level, genData_rain10

#获取数据, 处理数据, 存储数据, 数据装块
def genData(numOfX,numOfY,preTime,deviceID):
    mod1=0
    mod2=preTime%5
    stationID=read_WDRS(deviceID)

    # 获取数据
    
    origin_wl=get_waterlevel(deviceID)
    origin_rf,sort=get_rainfall(stationID)
    # 处理数据, 存储数据, 获取数据
    '''
    norm_wl_now=norm_waterlevel(origin_wl,deviceID,mod1)
    if mod2==mod1:
        norm_wl_pre=norm_wl_now
    else:
    '''
    norm_wl_now=norm_waterlevel(origin_wl,deviceID,mod1)
    if mod2==mod1:
        norm_wl_pre=norm_wl_now
    else:
        norm_wl_pre=norm_waterlevel(origin_wl,deviceID,mod2)
    norm_rf=norm_rainfall(origin_rf,stationID,0)

    # 数据装块
    if int(sort)==0:
        dataSet=genData_rain10(numOfX,numOfY,norm_rf,norm_wl_pre,norm_wl_now,preTime)
        return dataSet
    else:
        raise BaseException("由于没有对应的非规划院数据集，使用非规划院降雨数据集进行装块的算法并未编写。")