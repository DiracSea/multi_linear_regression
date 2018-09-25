from data_construction_allInOne.vonorio import cfg
import MySQLdb as mdb
from data_construction_allInOne.vonorio import wdrs

def get_waterlevel(deviceID):
    deviceID=str(deviceID)
    DB=cfg.get_waterlevel_DB()
    connect = mdb.connect(DB['host'],DB['usr'],DB['pwd'],DB['name'],int(DB['port']),charset='utf8')
    with connect:
        cur = connect.cursor()
        cur.execute("SELECT TIME1, WATER_HEIGHT FROM "+DB['table']+" where SENSORCODE = "+deviceID)
        rows=cur.fetchall()
    return list(rows)
    
def get_rainfall(stationID):
    stationID=str(stationID)
    DB=cfg.get_rainfall_DB()
    connect = mdb.connect(DB['host'],DB['usr'],DB['pwd'],DB['name'],int(DB['port']),charset='utf8')
    
    if int(DB['sort'])==0:            
        with connect:
            cur = connect.cursor()
            cur.execute("SELECT cur_start_t, cur_ter_t, rainfall, one_hr_start_t, one_hr_ter_t, one_hr_rainfall, three_hrs_start_t, three_hrs_ter_t, three_hrs_rainfall FROM "+DB['table']+" where STATION = '"+stationID+"'")
            rows=cur.fetchall()
    else:
        with connect:
            cur = connect.cursor()
            cur.execute("SELECT collectTime, curValue FROM "+DB['table']+" partition(P%s)"%stationID)
            rows=cur.fetchall()

    return list(rows), DB['sort']