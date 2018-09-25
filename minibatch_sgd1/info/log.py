from minibatch_sgd1.info.time import current_time
from minibatch_sgd1.info.format import de_norm

def write_log(flag,path,t,basic_param,m,result_param=0,R1=0,value=0,a_pred=0,analyze_param=0):
    with open(path,'a+') as f:
        f.write('times:'+str(t)+'\n')
        f.write('current_time:'+current_time().strftime('%Y-%m-%d %H:%M:%S')+'\n')
        if flag == 1:
            f.write('name:'+str(basic_param[0]))
            f.write(',batchsize:'+str(basic_param[1])+',epochs:'+str(basic_param[2])+',rate:'+str(basic_param[3])+'\n')
            f.write('X:'+str(basic_param[4])+',Y:'+str(basic_param[5])+',per_time:'+str(basic_param[6])+'\n')
            f.write('min:'+str(m[0])+',max:'+str(m[1])+'\n')
        if flag == 2 or flag == 3:
            f.write('A_inital:'+str(result_param[0])+',b_inital:'+str(result_param[1])+'\n')
            f.write('A:'+str(result_param[2])+',b:'+str(result_param[3])+'\n')
            f.write('l_train:'+str(result_param[4])+',l_valid:'+str(result_param[5])+'\n')
            f.write('MAE:'+str(de_norm(value[0],m))+',RMSE:'+str(de_norm(value[1],m))+',R:'+str(value[2])+',adjust_R:'+str(R1)+',CE:'+str(value[3])+'\n')
        if flag == 3:
            f.write('a_pred:'+str(a_pred[0])+',b_pred:'+str(analyze_param[0])+',R_pred:'+str(analyze_param[1])+',adjust_R:'+str(analyze_param[2])+'\n')
        f.write('----------------------')

    