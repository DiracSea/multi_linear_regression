#this is minibatch algorithm which is rewrited from minibatch and read data directly from caoz
import os
import numpy as np
import matplotlib.pyplot as plt
from minibatch_sgd1.data_process.fetch_data import use_data,use_data1
from minibatch_sgd1.minibatch import scale,calibrate,validate,evaluate,predict_regression,obs_pred_compare,adjust_R
from minibatch_sgd1.info.time import current_time
from minibatch_sgd1.info.plot import draw_plot
from minibatch_sgd1.info.log import write_log

def divide(input):
    X = input[:,:-1]
    y = input[:,-1]
    return X,y

def rand_select_batch(T,batchsize):
    np.random.shuffle(T)
    return T[:batchsize,:]


def run(X_num,Y_num,pertime,batchsize,epochs,rate,name,gen,b = 0.5,A = []):
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

    T,V,m = use_data1(pertime,name)
    
    if T != []:
        Xv,yv = divide(V)
        my_path = os.path.abspath(os.path.dirname(__file__))
        t = current_time().strftime("%Y%m%d_%H%M%S")
        logname = str(name)+'_'+str(X_num)+'_'+str(Y_num)+'_'+str(pertime)+'_'+t

        path = 'C:\\Users\\Administrator\\Documents\\data\\old\\'
        path1 = os.path.join(my_path, "data\\log\\"+'log_'+logname+'.txt')
        path2 = os.path.join(my_path, "data\\graph\\")
        path3 = os.path.join(my_path, "data\\list\\")

        sort_flag = 0;times0=0
        A0=0;b0=0;result_param0=0;value0=np.zeros(4)
        all_step0=0;train_loss0=0;valid_loss0=0

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

        flag = draw_plot(m,path,flag,pertime,path2,logname,yv,y_pred,all_step0,train_loss0,valid_loss0,a_pred,b_pred)


        y_pred_all.append(y_pred)
        
        y_pred_all = np.array(y_pred_all)
        y_pred_all = y_pred_all*(m[1]-m[0])+m[0]
        y_pred_all = np.int64(y_pred_all>0)

        '''
        pertime = np.array(pertime)
        y_pred_all = np.array(y_pred_all)
        y_pred = np.row_stack(pertime,y_pred_all)
        '''

        return A0,b0,y_pred_all,path3
    else:
        return [],0,[],""
'''
    print('A:',A)
    print('b:',b)
    print('l_train:',l_train)
    print('l_val:',l_val)
    return A,b,l_train,l_val
'''
    