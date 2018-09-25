
from minibatch_sgd.direct_minibatch import run
import pandas as pd
'''
sensorlist = range(1,245)
batchsize=400
epochs=800
rate=0.02
#X_num_list = range(1,5)
X_num = 1;Y_num = 2
pertime = list(range(1,25))
time = 15
for sensorcode in sensorlist:
    print(str(sensorcode)+'\n')
    A,b,y_pred,path = run(X_num,Y_num,pertime,batchsize,epochs,rate,sensorcode,time)#,module,b=0.0099611026629,A=[ 0.34195712 , 0.65481618 , 0.27454597])
    if b != 0:
        dataframe = pd.DataFrame({'15':y_pred[0],'30':y_pred[1],'60':y_pred[2],'120':y_pred[3]})
        dataframe.to_csv(path+str(sensorcode)+".csv",index=False,sep=',')
'''
path = 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\stat_under_2018.csv'
sensorlist = pd.read_csv(path,encoding='gbk')['DEVICE_NAME'].tolist()
batchsize=400
epochs=800
rate=0.02
#X_num_list = range(1,5)
inputlist = [[1,2],[3,3],[6,6]]
timelist = [15,30,60]
time = 10
for input in inputlist:
    for sensorcode in sensorlist:
        for pertime in timelist:
            print(str(sensorcode)+'\n')
            run(input,pertime,batchsize,epochs,rate,sensorcode,time)#,module,b=0.0099611026629,A=[ 0.34195712 , 0.65481618 , 0.27454597])