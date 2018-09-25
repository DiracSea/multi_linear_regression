from minibatch_sgd.data_process.tool.sperate import split_num
from minibatch_sgd.data_process.tool.combine import first_stack
import numpy as np
from data_construction_allInOne import genData
from data_construction_allInOne.error import EmptyRainfallError,EmptyWaterlevelError,NoMethodError


def find_M(list):
    min0 = min(list)
    max0 = max(list)
    return min0,max0

def single_norm(list):
    min,max = find_M(list)
    new_list = []
    if min == max:
        return []
    else:
        for i in list:
            new_list.append((i-min)/(max-min))
        return new_list

def all_norm(nlist):
    tmp = map(list,zip(*nlist))
    nlist_T = list(tmp)
    m_nlist = map(find_M,nlist_T)
    m = list(m_nlist)[-1]

    if m[0] == m[1]:
        return [],[]
    
    else:
        new_nlist = map(single_norm,nlist_T)
        new_nlist_T = map(list,zip(*new_nlist))

        return list(new_nlist_T),m

def use_data(X_num,Y_num,pretime,name):
    try:
        table = genData(X_num,Y_num,pretime,name)
    except EmptyRainfallError as e:
        print("EmptyRainfallError:",e)
        return [],[],[]
    except EmptyWaterlevelError as e:
        print("EmptyWaterlevelError:",e)
        return [],[],[]
    except NoMethodError as e:
        print("NomethodError:",e)
        return [],[],[]
    else:
        nlist_T,m = all_norm(table)
        if m == []:
            return [],[],[]
        
        else:
            l = len(table)
            train_num,valid_num = split_num(l)
            norm_table = list(nlist_T)
            new_table = np.array(norm_table)#[:,1:]
            T = [];V = [];flag = 1;flag1 = 1
            counter = 0
            for row in new_table:
                counter += 1
                if counter < train_num:
                    T,flag = first_stack(T,row,flag)
                else:
                    V,flag1 = first_stack(V,row,flag1)
            return T,V,m
        
        

