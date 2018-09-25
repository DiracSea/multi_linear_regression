#this is minibatch algorithm which is rewrited from minibatch and read data directly from caoz
import os
import numpy as np
import matplotlib.pyplot as plt
import csv

from minibatch_sgd.data_process.fetch_data import use_data
from minibatch_sgd.minibatch import scale,calibrate,validate,evaluate,predict_regression
from minibatch_sgd.data_process.tool.combine import remove_and_combine
from minibatch_sgd.info.format import large_than_0

def divide(input):
    X = input[:,:-1]
    y = input[:,-1]
    return X,y

def rand_select_batch(T,batchsize):
    np.random.shuffle(T)
    return T[:batchsize,:]

def multi_predict(A,b,X,X_num,time):
    y = 0
    for i in range(time):
        if i == 0:
            y = predict_regression(A,b,X)
        else:
            X_new = remove_and_combine(X,y,X_num)
            X = np.array(X_new)
            y = predict_regression(A,b,X)
        yield y

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

    l = len(pertime)
    T,V,m = use_data(X_num,Y_num,5,name)
    
    if T != []:
        Xv,yv = divide(V)#Xv is vector,yv is scalar
        my_path = os.path.abspath(os.path.dirname(__file__))

        #path1 = os.path.join(my_path, "data\\log\\"+'log_'+logname+'.txt')
        #path2 = os.path.join(my_path, "data\\graph\\")
        path = os.path.join(my_path, "data\\list\\")

        sort_flag = 0;times0=0
        A0=0;b0=0;result_param0=0;value0=np.zeros(4)
        all_step0=0;train_loss0=0;valid_loss0=0

        if A != []:
            gen = 1

        
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
         
            if sort_flag == 0:
                value0 = value
                sort_flag = 1
                times0 = times
                A0 = A;b0 = b
                all_step0=all_step;train_loss0=train_loss;valid_loss0=valid_loss

            if value[0]<value0[0] and value[2]>0.9 and value[3]>0.6:
                value0 = value;times0 = times
                A0 = A;b0 = b
                all_step0=all_step;train_loss0=train_loss;valid_loss0=valid_loss


        flag = 0
        X_in = Xv[0]
        y_pred_all = np.array(list(multi_predict(A0,b0,X_in,X_num,l)))
        y_pred_all = y_pred_all*(m[1]-m[0])+m[0]
        y_pred_all = large_than_0(y_pred_all)

        '''
        pertime = np.array(pertime)
        y_pred_all = np.array(y_pred_all)
        y_pred = np.row_stack(pertime,y_pred_all)
        '''
        
        with open(path+"predict.csv",'a',newline='') as f:
            writer = csv.writer(f)
            if name == 1:
                pertime = np.array(pertime)
                pertime = list(map(str,pertime*5))
                pertime.insert(0,'编号\分钟')
                writer.writerow(pertime)

            y_pred_all.insert(0,name)
            writer.writerow(y_pred_all)

        with open(path+"sample.csv",'a',newline='') as f:
            writer = csv.writer(f)
            if name == 1:
                writer.writerow(pertime)

            tmp = np.array(yv[0:l])*(m[1]-m[0])+m[0]
            tmp = list(tmp)
            tmp.insert(0,name)
            writer.writerow(tmp)

    pass

    