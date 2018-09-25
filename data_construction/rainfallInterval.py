import csv
import os

def rainfallInterval(fileName):
    my_path = os.path.abspath(os.path.dirname(__file__))
    inputName = os.path.join(my_path,'inputRainfall\\'+fileName)
    #inputName='.\\data_construction\\'
    #outputName='.\\output-rainfallInterval\\'+fileName+'eachRain.csv'

    #读取数据到内存
    data=[]
    csv_file=csv.reader(open(inputName,'r'))
    count=0
    for i in csv_file:
        if count==0:
            count=count+1
        else:
            precip=float(i[6])
            if precip<=0.02:#小于多少值的降雨量直接忽略为0
                precip=0
            data.append([i[4],i[5],precip])

    #开始判断是否为一场雨
    checkList=[]
    m=len(data)
    judgeInt=12#至少多久不下雨才会分为两场雨，12代表12个十分钟，也就是2小时
    ifPattern=judgeInt+1#用于判断是否属于同一个场雨中，初始为不属于(大于judgeInt为不属于,小于等于为属于)
    minInt=6#下雨持续超过1小时，才会被使用。
    start=0#数据初始化
    end=m#数据初始化

    for i in range(m):#代码类似于处理降雨量数据集时的checkArray
        if data[i][2]!=0:
            if ifPattern>=judgeInt:
                start=i
                end=i
            else:
                end=i
            ifPattern=0
            if i==m-1:#与checkArray同理，最后一个值不为负的情况，也要加上去
                if end-start>=minInt-1:
                    checkList.append([start,end])
        else:
            ifPattern=ifPattern+1
            if (ifPattern==judgeInt) & (data[start][2]!=0):#当零点记数第一次大于judgeInt时，记录对应的雨型时刻
                if end-start>=minInt-1:
                    checkList.append([start,end])

    return (checkList,data)
    
    # #根据check的结果，导出场雨数据
    # eachRainData=[]
    # m=len(checkList)
    # for i in range(m):
    #     for j in range(checkList[i][0],checkList[i][1]+1):
    #         eachRainData.append([str(i+1)]+data[j])

    # m = len(eachRainData)
    # n = len(eachRainData[0]) #因为存在标签，所以这里直接给明需要的数据列数
    # with open(outputName, 'w') as f:
    #     for j in range(m):
    #         for k in range(n-1):
    #             f.write(str(eachRainData[j][k])+',')
    #         f.write(str(eachRainData[j][n-1]))
    #         f.write('\n')

# for i in os.listdir(r'.\inputRainfall'):
#     print('#########################')
#     rainfallInterval(i)
#     print('Mission %s is completed successfully!\n'%i)