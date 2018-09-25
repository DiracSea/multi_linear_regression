#this is minibatch algorithm which is rewrited from minibatch and read data directly from caoz
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from minibatch_sgd.data_process.fetch_data import use_data
from minibatch_sgd.minibatch import scale,calibrate,validate,evaluate,predict_regression,obs_pred_compare,adjust_R
from minibatch_sgd.info.time import current_time
from minibatch_sgd.info.plot import draw_plot
from minibatch_sgd.info.log import write_log

def divide(input):
    X = input[:,:-1]
    y = input[:,-1]
    return X,y

def rand_select_batch(T,batchsize):
    np.random.shuffle(T)
    return T[:batchsize,:]


def run(input,pertime,batchsize,epochs,rate,name,gen,b = 0.5,A = []):
    """
    :param X_num
    :param Y_num
    :param pertime
    :param batchsize
    :param epochs
    :param rate
    :param name
    :param gen 
    :param A
    :param b
    :return:
    """
    X_num = input[0];Y_num = input[1]
    T,V,m = use_data(X_num,Y_num,pertime,name)
    
    if T != []:
        Xv,yv = divide(V)
        my_path = os.path.abspath(os.path.dirname(__file__))
        t = current_time().strftime("%Y%m%d_%H%M%S")
        logname = str(name)+'_X'+str(X_num)+'_Y'+str(Y_num)+'_time'+str(pertime)+'_'+t

        path1 = os.path.join(my_path, "data\\log\\"+'log_'+logname+'.txt')
        path2 = os.path.join(my_path, "data\\graph\\")
        path3 = os.path.join(my_path, "data\\result\\")

        sort_flag = 0;times0=0
        A0=0;b0=0;result_param0=0;value0=np.zeros(4)
        all_step0=0;train_loss0=0;valid_loss0=0;value = []

        if A != []:
            gen = 1

        basic_param = [name,batchsize,epochs,rate,X_num,Y_num,pertime]
        write_log(1,path1,'inital',basic_param,m)

        
        for times in range(1,gen+1):
            A = [];b = 0
            all_step = []; train_loss = []; valid_loss = [];A1 = A;b1 = b
            #loss_t = 1
            for i in range(epochs):
                batch = rand_select_batch(T,batchsize)
                X,y = divide(batch)
                if A == [] or len(A) != len(X[0]):
                    A,b = scale(X)
                    A1 = A;b1 = b
                
                A,b,loss_t = calibrate(X,y,A,b,rate)
                loss_v = validate(Xv,yv,A,b)

                all_step.append(i)
                train_loss.append(loss_t)
                valid_loss.append(loss_v)

                # with open(path,'a') as f:
                #     f.write('epochs:'+str(i)+',train_loss:'+str(loss_t)+',validation_loss:'+str(loss_v)+'\n')


            l_train = sum(train_loss)/epochs
            l_val = loss_v
            value = evaluate(Xv,yv,A,b)

            result_param = [A1,b1,A,b,l_train,l_val]
            R1 = adjust_R(value[2],X_num,Y_num,len(yv))

            write_log(2,path1,times,basic_param,m,result_param,R1,value)
            
            if sort_flag == 0:
                value0 = value
                sort_flag = 1
                times0 = times
                A0 = A;b0 = b;result_param0 = result_param
                all_step0=all_step;train_loss0=train_loss;valid_loss0=valid_loss

            if value[0]<value0[0] and value[2]>0.9 and value[3]>0.5:
                value0 = value;times0 = times
                A0 = A;b0 = b;result_param0 = result_param
                all_step0=all_step;train_loss0=train_loss;valid_loss0=valid_loss


        flag = 0
        y_pred_all = []

        y_pred = predict_regression(A0,b0,Xv)
        a_pred,b_pred,R_pred = obs_pred_compare(yv,y_pred)

        R1 = adjust_R(value0[2],X_num,Y_num,len(yv))
        R2 = adjust_R(R_pred,1,0,len(yv))

        analyze_param = [b_pred,R_pred,R2]
        
        write_log(3,path1,str(pertime)+'min',basic_param,m,result_param0,R1,value0,a_pred,analyze_param)

        flag = draw_plot(flag,pertime,path2,logname,yv,y_pred,all_step0,train_loss0,valid_loss0,a_pred,b_pred)

        with open(path3+'result.csv','a',newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=",")
            param = ''
            for i in A0:
                param+=(str(i)+';')
            line = [name,pertime,X_num,Y_num,param,b0,m[0],m[1],value[0],value[2],value[3]]
            writer.writerow(line)
        pass
