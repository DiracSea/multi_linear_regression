import numpy as np

#注：方程的y值可作为额外列输入。但如果方程无解，不会报错，所得方程矩阵错。
def gaussianElimination(matrix,isHaveY='N'):
    matrix=matrix.astype('float32')
    (rows,cols)=matrix.shape
    if isHaveY == 'Y':
        cols=cols-1 
    isPivot=np.zeros(cols)
    curRow=0
    for curCol in range(cols):
        extraRow=matrix[curRow:,curCol]
        relaPivot=np.argwhere(extraRow!=0)

        if len(relaPivot)!=0:
            pivotIndex=curRow+relaPivot[0,0]
            isPivot[curCol]=True
            matrix[[curRow,pivotIndex]]=matrix[[pivotIndex,curRow]]
            matrix[curRow]=matrix[curRow]/matrix[curRow,curCol]
            for i in np.delete(np.arange(rows),curRow):
                matrix[i]=matrix[i]-matrix[i,curCol]*matrix[curRow]
            curRow=curRow+1

    return matrix