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
import csv
import pandas as pd
from data_construction_allInOne.gaussian import solve_rainfall
#{cur_start_t,cur_ter_t,rainfall,one_hr_start_t,one_hr_ter_t,one_hr_rainfall,three_hrs_start_t,three_hrs_ter_t,three_hrs_rainfall}
path1 = 'C:\\Users\\Administrator\\Documents\\Python Scripts\\data\\hualinglu\\rain2018'
path2 = 'C:\\Users\\Administrator\\Documents\\Python Scripts\\data\\hualinglu\\level2018'

def get_df(name,time):
    '''
    :param name {'rain','level'}
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

df = get_df('rain',7)
a = solve_rainfall()