import numpy as np

def first_stack(X1,X2,flag):
    if flag:
        flag = 0
        X1 = X2
    else:
        X1 = np.row_stack((X1,X2))
    return X1,flag


def remove_and_combine(X,y,X_num):
    if X.ndim == 1:
        X_new = list(X)
        del X_new[X_num]
        X_new.append(y)
    else:
        X_new = np.delete(X,X_num,1)
        X_new = np.column_stack((X_new,y))
    return X_new
