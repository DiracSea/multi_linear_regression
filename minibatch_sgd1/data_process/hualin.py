'''
from minibatch_sgd.sample_minibatch import run

sensorlist = range(54,245)
batchsize=400
epochs=800
rate=0.02
#X_num_list = range(1,5)
X_num = 1;Y_num = 2
pertime = list(range(1,25))
time = 8
for sensorcode in sensorlist:
    print(str(sensorcode)+'\n')
    run(X_num,Y_num,pertime,batchsize,epochs,rate,sensorcode,time)
'''
import datetime
import csv
import pandas as pd
import numpy as np
from data_construction_allInOne.gaussian import solve_rainfall
from data_construction_allInOne.gaussian.timeNorm import getTime
from data_construction_allInOne.tmp import norm_waterlevel,norm_rainfall
from data_construction_allInOne.interpolation import interpolation
from data_construction_allInOne.timeNorm import getTime
from data_construction_allInOne.corrData import rain10_level, genData_rain10
#{cur_start_t,cur_ter_t,rainfall,one_hr_start_t,one_hr_ter_t,one_hr_rainfall,three_hrs_start_t,three_hrs_ter_t,three_hrs_rainfall}
path = 'C:\\Users\\Administrator\\Documents\\Python Scripts\\data\\hualinglu\\'
path1 = 'C:\\Users\\Administrator\\Documents\\Python Scripts\\data\\hualinglu\\rain2018'
path2 = 'C:\\Users\\Administrator\\Documents\\Python Scripts\\data\\hualinglu\\level2018'
level = ('华林路晋安河','华林路YS3283260011','华林路YS3293240001','华林路YS3233270040','华林路YS3253270069')
def get_df(name,time):
    '''
    :param name {'rain','level','road'}
    :param time {5,6,7}
    '''
    s = '.csv'
    if name == 'rain':
        path = path1
        if time == 5:
            t = '05'
        elif time == 6:
            t = '06'
        elif time == 7:
            t = '07'
        return pd.read_csv(path+t+s,encoding='gbk')
    elif name == 'level':
        path = path2
        if time == 5:
            t = '05'
        elif time == 6:
            t = '06'
        elif time == 7:
            t = '07'
        return pd.read_csv(path+t+s,encoding='gbk')

def to_date(l):
    line = []
    i = 0
    for t in l:
        if i == 2 or i == 5 or i == 8:
            line.append(t)
        else:
            line.append(getTime(t))
        i+=1
    return line
'''
df1 = get_df('rain',5)
df2 = get_df('rain',6)
df3 = get_df('rain',7)

r1 = df1.append(df2)
r2 = r1.append(df3)


l = np.array(r2).tolist()
new_list = list(map(to_date,l))
#print(l)

rain = solve_rainfall(*new_list)
'''
'''
df1 = get_df('level',5)
df2 = get_df('level',6)
df3 = get_df('level',7)

r1 = df1.append(df2)
r2 = r1.append(df3)
'''
'''
for l in level:
    idx = r2['DEVICE_NAME'] == l
    r2[idx][['TIME','WATER_HEIGHT']].to_csv(path+l+'.csv',index=False)
'''
def str2time(row):
    time = getTime(row[0])
    return [time,row[1]]
def neg2zero(row):
    if row[1] < 0:
        tmp = 0
    else:
        tmp = row[1]
    return [row[0],tmp]
'''
for l in level:
    f = open(path+l+'.csv')
    df = np.array(pd.read_csv(f)).tolist()
    #print(df)
    df = list(map(str2time,df))
    df = list(map(neg2zero,df))
    a = interpolation(0,df)
    a = list(map(neg2zero,a))
    tmp = list(map(list,zip(*a)))
    df = pd.DataFrame({'time':tmp[0],'value':tmp[1]})
    df.to_csv(path+l+'_norm.csv',index=0)
'''
def genData(pretime,l):
    rainfall =  np.array(pd.read_csv(path+'rainfall.csv')).tolist()
    f = open(path+l+'_norm.csv')
    df = np.array(pd.read_csv(f)).tolist()
    a = genData_rain10(2,2,rainfall,df,df,pretime)
    return a


    