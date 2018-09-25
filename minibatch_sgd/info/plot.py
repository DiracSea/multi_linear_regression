from minibatch_sgd.info.time import current_time
from sklearn import linear_model
import matplotlib.pyplot as plt

def draw_plot(flag,pertime,path,logname,yv,y_pred,all_step,train_loss,valid_loss,a_pred,b_pred):

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

    logname = logname+'_'+str(pertime)
    regr = linear_model.LinearRegression()
    step = list(range(len(yv)))
    yv_pred = a_pred*yv+b_pred

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