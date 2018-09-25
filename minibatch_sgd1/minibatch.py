import numpy as np
import random
import matplotlib.pyplot as plt
import logging
import math
from sklearn import linear_model
from sklearn.metrics import r2_score
from minibatch_sgd1.data_process.tool.combine import first_stack,remove_and_combine
#A is row vector
#X is column vector, rainfall
#y is water
'''
def eva_func(category):
    try:
        return {
            'MAE': MAE,#mean absolute error
            'RMSE': RMSE,#root mean square error
            'R': R,#coefficient of correlation :close to 1 is better
            'CE': CE#coefficient of effficiency :close to 1 is better
        }[category]
    except KeyError:
        print('input is wrong')
'''
def yp(A,b,X):
    return np.dot(A,X) + b

def mean_yp(A,b,Xv):
    yp_ = 0;i = 0
    for i in range(len(Xv)):
        yp_+=yp(A,b,Xv[i])
    i+=1
    return yp_/i
    
def mean_y(yv):
    return np.mean(yv)

def dA(y,y_p,X):#negative partial A/gradA, A is vector
    return (y-y_p)*(-X)

def db(y,y_p):#negative partial b/gradb
    return (y-y_p)*(-1)

def MAE(Xv,yv,A,b):
    loss = 0;i = 0
    for i in range(len(Xv)):

        yv_p = yp(A,b,Xv[i])
        loss += abs(yv[i]-yv_p)
    i+=1
    return loss/i

def RMSE(Xv,yv,A,b):
    loss = 0;i = 0
    for i in range(len(Xv)):
        yv_p = yp(A,b,Xv[i])
        loss += (yv[i] - yv_p)*(yv[i] - yv_p)
    i+=1
    loss = math.sqrt(loss/i)
    return loss

def R(Xv,yv,A,b):
    yv_p_ = mean_yp(A,b,Xv)
    yv_ =mean_y(yv)
    R1 = 0;R2 = 0;R3 = 0
    for i in range(len(Xv)):
        yv_p = yp(A,b,Xv[i])
        R1 += (yv_p-yv_p_)*(yv[i]-yv_)
        R2 += (yv_p-yv_p_)*(yv_p-yv_p_)
        R3 += (yv[i]-yv_)*(yv[i]-yv_)
    R = R1/math.sqrt(R2*R3)
    return R

def adjust_R(R,X_num,Y_num,num):
    return 1-(1-R*R)*(num-1)/(num-X_num-Y_num-1)

def CE(Xv,yv,A,b):
    yv_ =mean_y(yv)
    CE1 = 0;CE2 = 0
    for i in range(len(Xv)):
        yv_p = yp(A,b,Xv[i])
        CE1 += (yv[i]-yv_p)*(yv[i]-yv_p)
        CE2 += (yv[i]-yv_)*(yv[i]-yv_)
    return 1-CE1/CE2

def regular():
    pass


def scale(X):
    l = len(X[0])
    #A = np.ones(l)*0.5#*A_scale
    #b = 0.5#*b_scale
    #A = np.zeros(l)
    #b = 0
    A = np.random.rand(l)
    b = random.random()
    return A,b
    

def log(epochs,l_train,l_val):
    logging.info('epoch:' + str(epochs) + ' ,train_loss:' + str(l_train) + ' ,val_loss:' + str(l_val))


def calibrate(X,y,A,b,rate):#X, y is batch
    all_dA = np.zeros(np.shape(A))
    all_db = 0
    loss = 0

    for i in range(len(X)):
        y_p = yp(A,b,X[i])
        loss = loss + (y[i] - y_p)*(y[i] - y_p)/2
        all_dA = all_dA + dA(y[i],y_p,X[i])
        all_db = all_db + db(y[i],y_p)
    
    loss = loss/len(X)
    
    #if(loss < loss0):
    #    rate /= 5
    A = A - rate*all_dA/len(X)
    b = b - rate*all_db/len(X)
    return A,b,loss

def validate(Xv,yv,A,b):
    loss = 0
    i = 0
    for i in range(len(Xv)):
        yv_p = yp(A,b,Xv[i])
        loss += (yv[i] - yv_p)*(yv[i] - yv_p)/2
    i+=1
    loss = loss/i
    return loss


def evaluate(Xv,yv,A,b):
    eva_func = [MAE,RMSE,R,CE]
    value = []
    for func in eva_func:
        value.append(func(Xv,yv,A,b))
    return value


def predict_regression(A,b,X):
    if X.ndim == 1:
        y_pred = np.dot(A,X)+b
    else:
        tmp = map(lambda x: np.dot(A,x)+b,X)
        y_pred = list(tmp)

    return y_pred

def obs_pred_compare(y_obs,y_pred):#use sklearn pack to save time

    regr = linear_model.LinearRegression()
    regr.fit(y_obs.reshape(-1,1),y_pred)#y_obs is 1 dimension
    a, b = regr.coef_, regr.intercept_
    R = r2_score(y_obs,y_pred)
    return a,b,R


'''
def multi_predict(A,b,X,X_num,time):
    y = predict_regression(A,b,X)
    if time>1:
        for i in range(time-1):
            X_new = remove_and_combine(X,y,X_num)
            y = predict_regression(A,b,X_new)
    return y
'''