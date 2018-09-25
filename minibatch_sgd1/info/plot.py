from minibatch_sgd1.info.time import current_time
from sklearn import linear_model
import matplotlib.pyplot as plt
import pandas as pd

def draw_plot(m,p,flag,pertime,path,logname,yv,y_pred,all_step,train_loss,valid_loss,a_pred,b_pred):
    logname = logname+'_'+str(pertime)
    regr = linear_model.LinearRegression()
    step = list(range(len(yv)))
    yv_pred = a_pred*yv+b_pred
    '''
    yv = (m[1]-m[0])*yv + m[0]
    yv_pred = (m[1]-m[0])*yv_pred + m[0]
    '''
    if flag == 0:
        flag = 1
        plt.figure()
        plt.plot(all_step,train_loss,color = 'blue',label = 'train')
        plt.plot(all_step,valid_loss,color = 'red', label = 'validation')
        plt.xlabel('step')
        plt.ylabel('loss')
        plt.legend()
        #plt.ylim(0,0.05)
        plt.savefig(path+'plot_'+logname+'.png')####
        plt.close('all')
        tmp = pd.DataFrame({'train_loss':train_loss,'validation_loss':valid_loss})
        tmp.to_csv(p+logname+'.csv')
        tmp = pd.DataFrame({'observe':yv,'predict':yv_pred})
        tmp.to_csv(p+logname+'_data'+'.csv')



    plt.figure()
    figsize = (13,10)  
    plt.scatter(step,yv,color='blue',label='observed value')
    plt.scatter(step,y_pred,color='red',marker = 'x',label='predicted value')
    plt.xlim(-50,len(yv)+50)
    plt.xlabel('Time')
    plt.ylabel('Level')
    plt.legend()
    plt.savefig(path+'plot_pred_'+logname+'.png')####
    plt.close('all')

    plt.figure()
    figsize = (11,9)  
    plt.scatter(yv,y_pred,color='blue',label='point')
    plt.plot(yv,yv_pred,color='red',label='linear_model')
    plt.xlabel('y_observe')
    plt.ylabel('y_predict')
    plt.legend()
    plt.savefig(path+'plot_regr_'+logname+'.png')####
    plt.close('all')
    return flag