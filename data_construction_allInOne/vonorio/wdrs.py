from data_construction_allInOne.vonorio import cfg
import MySQLdb as mdb
import numpy as np

def get_RStation():
    DB=cfg.find_RStation_LOCDB()
    connect = mdb.connect(DB['host'],DB['usr'],DB['pwd'],DB['name'],int(DB['port']),charset='utf8')
    with connect:
        cur = connect.cursor()
        cur.execute("SELECT DEVICE_NAME,X,Y FROM "+DB['table'])
        rows=cur.fetchall()
    return rows

def get_WDevice():
    DB=cfg.find_WDevice_LOCDB()
    connect = mdb.connect(DB['host'],DB['usr'],DB['pwd'],DB['name'],int(DB['port']),charset='utf8')
    with connect:
        cur = connect.cursor()
        cur.execute("SELECT DEVICE_NAME,X,Y FROM "+DB['table'])
        rows=cur.fetchall()
    return rows

def find_WDevice(deviceID):
    WDevices=get_WDevice()
    ifexist=False
    for row in WDevices:
        if str(row[0])==str(deviceID):
            ifexist=True
            break
    return ifexist

def eucliDist(x1,x2,y1,y2):
    x1=float(x1)
    x2=float(x2)
    y1=float(y1)
    y2=float(y2)
    return ((x1-x2)**2+(y1-y2)**2)**0.5

def get_WDRS():
    RStations=get_RStation()
    WDevices=get_WDevice()
    m=len(RStations)
    n=len(WDevices)
    dist_matrix=np.ones((m,n))
    for i in range(m):
        x1=RStations[i][1]
        y1=RStations[i][2]
        for j in range(n):
            x2=WDevices[j][1]
            y2=WDevices[j][2]
            dist_matrix[i,j]=eucliDist(x1,x2,y1,y2)
    nearest=dist_matrix.argmin(axis=0)

    WD_RS=[]
    for i in range(n):
        corr_WDevice=nearest[i]
        WD_RS.append([WDevices[i][0],RStations[corr_WDevice][0]])
    
    return WD_RS