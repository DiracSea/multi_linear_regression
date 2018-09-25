import os
import configparser
from data_construction_allInOne.vonorio import wdrs

curr_path=(os.path.split(__file__))[0]
CONFIG_FILE = os.path.join(curr_path,"data.cfg")
WDRS_FILE = os.path.join(curr_path,"WDRS.cfg")
prefix="wdevices_"

def find_RStation_LOCDB():
    conf = configparser.ConfigParser()  
    try:
        conf.read(CONFIG_FILE)
        sec_name="rainfall_station_LOCDB"
        host = conf.get(sec_name, "DATABASE_HOST")
        port = conf.get(sec_name, "DATABASE_PORT")
        name = conf.get(sec_name, "DATABASE_NAME")
        usr = conf.get(sec_name, "DATABASE_USERNAME")
        pwd = conf.get(sec_name, "DATABASE_PASSWORD")
        table = conf.get(sec_name, "DATABASE_TABLE")
    
        return {'host':host,'port':port,'name':name,'usr':usr,'pwd':pwd,'table':table}
    except BaseException as e:
        if os.path.exists(CONFIG_FILE):
            print("Config file Error: %s"%CONFIG_FILE)
            print(e)
        else:
            print("Missing Config file: %s"%CONFIG_FILE)
        exit()

def find_WDevice_LOCDB():
    conf = configparser.ConfigParser()  
    try:
        conf.read(CONFIG_FILE)
        sec_name="water_device_LOCDB"
        host = conf.get(sec_name, "DATABASE_HOST")
        port = conf.get(sec_name, "DATABASE_PORT")
        name = conf.get(sec_name, "DATABASE_NAME")
        usr = conf.get(sec_name, "DATABASE_USERNAME")
        pwd = conf.get(sec_name, "DATABASE_PASSWORD")
        table = conf.get(sec_name, "DATABASE_TABLE")
    
        return {'host':host,'port':port,'name':name,'usr':usr,'pwd':pwd,'table':table}
    except BaseException as e:
        if os.path.exists(CONFIG_FILE):
            print("Config file Error: %s"%CONFIG_FILE)
            print(e)
        else:
            print("Missing Config file: %s"%CONFIG_FILE)
        exit()

def get_rainfall_DB():
    conf = configparser.ConfigParser()  
    try:
        conf.read(CONFIG_FILE)
        sec_name="rainfall_DB"
        # 0代表为规划院数据。其他整数为所使用的间隔雨量数据，例，5代表使用的为间隔为5分钟的雨量数据。
        sort = conf.get(sec_name, "DATABASE_SORT")
        host = conf.get(sec_name, "DATABASE_HOST")
        port = conf.get(sec_name, "DATABASE_PORT")
        name = conf.get(sec_name, "DATABASE_NAME")
        usr = conf.get(sec_name, "DATABASE_USERNAME")
        pwd = conf.get(sec_name, "DATABASE_PASSWORD")
        table = conf.get(sec_name, "DATABASE_TABLE")
    
        return {'sort':sort,'host':host,'port':port,'name':name,'usr':usr,'pwd':pwd,'table':table}
    except BaseException as e:
        if os.path.exists(CONFIG_FILE):
            print("Config file Error: %s"%CONFIG_FILE)
            print(e)
        else:
            print("Missing Config file: %s"%CONFIG_FILE)
        exit()

def get_waterlevel_DB():
    conf = configparser.ConfigParser()  
    try:
        conf.read(CONFIG_FILE)
        sec_name="waterlevel_DB"
        host = conf.get(sec_name, "DATABASE_HOST")
        port = conf.get(sec_name, "DATABASE_PORT")
        name = conf.get(sec_name, "DATABASE_NAME")
        usr = conf.get(sec_name, "DATABASE_USERNAME")
        pwd = conf.get(sec_name, "DATABASE_PASSWORD")
        table = conf.get(sec_name, "DATABASE_TABLE")
    
        return {'host':host,'port':port,'name':name,'usr':usr,'pwd':pwd,'table':table}
    except BaseException as e:
        if os.path.exists(CONFIG_FILE):
            print("Config file Error: %s"%CONFIG_FILE)
            print(e)
        else:
            print("Missing Config file: %s"%CONFIG_FILE)
        exit()

def write_WDRS():
    WDRS=wdrs.get_WDRS()
    #读取个人设置并临时存储
    conf=configparser.ConfigParser()
    conf.read(WDRS_FILE)
    My_configs=conf.items('My_configs')
    #重新写入文件
    conf=configparser.ConfigParser()
    with open(WDRS_FILE,'w') as f:
        conf.add_section('My_configs')
        for my_config in My_configs:
            wd=my_config[0][len(prefix):]
            rs=my_config[1]
            conf.set("My_configs",prefix+str(wd),str(rs))
        conf.add_section('WDevices_RStations')
        for i in WDRS:
            wd=i[0]
            rs=i[1]
            conf.set("WDevices_RStations",prefix+str(wd),str(rs))
                
        conf.write(f)

# 根据井盖号，找到对应的最近雨量站
def read_WDRS(deviceID):
    deviceID=str(deviceID)
    has_wd=check_WDRS(deviceID)
    if not has_wd:
        if wdrs.find_WDevice(deviceID):
            # 在位置数据库中发现了之前没有计算过的井盖，根据新的位置数据库更新所有的WD-RS
            write_WDRS()
            has_wd=check_WDRS(deviceID)
        else:
            raise BaseException("Failed to get the corresponding \
rainfall-station for device with poiID-%s. \
Please add its location in the location-database \
or modify my_config section in WDRS.cfg file."%deviceID)
            
    return has_wd

def check_WDRS(deviceID):
    deviceID=str(deviceID)
    has_wd=False

    conf=configparser.ConfigParser()
    conf.read(WDRS_FILE)
    has_wd1=conf.has_option("My_configs",prefix+deviceID)
    has_wd2=conf.has_option("WDevices_RStations",prefix+deviceID)
    if has_wd2:
        has_wd=conf.get("WDevices_RStations",prefix+deviceID)
    if has_wd1:
        has_wd=conf.get("My_configs",prefix+deviceID)

    return has_wd # 能在wdrs.cfg中找到则返回对应值，否则返回False