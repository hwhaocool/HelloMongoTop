#coding:utf-8

import subprocess
import logging
import time
import datetime
import pymongo
import simplejson
from urllib import quote_plus

from config import MyConfig
from MyDocument import MyDocument


logging.basicConfig(
    level = logging.INFO,
    format = '[%(asctime)s] - [%(filename)s] [%(levelname)s] - %(message)s'
    # datefmt = '%Y-%m-%d %A %H:%M:%S',
    )

logger = logging.getLogger(__name__)

def getTopOutput(cmd, sleeptime):
    '''1. 得到MongoTop 输出 (popen)'''
    proc = subprocess.Popen(cmd, \
                            shell=True, \
                            stdin=subprocess.PIPE, \
                            stdout=subprocess.PIPE, \
                            stderr=subprocess.PIPE)

    while True:
    # for i in range(5):
        time.sleep(sleeptime)
        current_out = proc.stdout.readline()
        analysisData(current_out)

def analysisData(data):
    '''2. 解析 data (json)'''
    now = datetime.datetime.now()
    
    print data
    
    if not len(data):
        logger.info("data is empty")
        return

    data_json = simplejson.loads(data)
    
    # 使用当前时间即可，免得转换
    current_time = now
    logger.info("mongotop output time is %s", current_time)

    totals_json = data_json["totals"]

    count = 0
    for key in totals_json.keys():
        if key.startswith("admin") or key.startswith("local"):
            continue
        datas = key.split(r".")
        database = datas[0]

        current_collection_name = datas[1]
        if current_collection_name == collection_name:
            #not record myself
            continue

        json_obj = totals_json[key]
        saveToDB(database, current_collection_name, json_obj, current_time)
        count = count + 1

    gap = (datetime.datetime.now() - now).microseconds / 1000

    logger.info("save %d ducuments cost %d ms", count, gap)

def saveToDB(database, current_collection_name, json_obj, current_time):
    '''3. 写入数据库 (dev mongodb)'''
    document = MyDocument(database, current_collection_name, json_obj, current_time)
    collection.insert_one(document.getJson())

# 4. 输出折线图到界面上（Flask）
def prettyPrint():
    #TODO: 折线图
    pass

def start(envType, sleeptime):
    '''开始入口，构造cmd'''
    # global var
    my_config = MyConfig()

    host = my_config.get(envType)['host']
    username = my_config.get(envType)['username']
    password = my_config.get(envType)['password']
    
    if 0 == sleeptime:
        sleeptime = my_config.get(envType)['sleeptime']
    
    #generate cmd
    # 执行 mongotop 需要账号可以访问 admin 库 权限
    my_cmd = "mongotop --host %s --username %s --password %s --authenticationDatabase=admin -vvvvv --json %d" \
        % (host, username, password,  sleeptime)

    # my_cmd = "/usr/bin/mongotop --version"

    logger.info("cmd is %s", my_cmd)

    #generate connection uri
    db_uri = my_config.get(envType)['dbUri']
    
    global collection_name
    collection_name = my_config.get(envType)['collection']
    
    # 数据写到 哪个库
    database = my_config.get(envType)['database']

    logger.info("db uri is %s", db_uri)
    client = pymongo.MongoClient(db_uri)
    db = client[database]
    global collection
    collection = db[collection_name]

    getTopOutput(my_cmd, sleeptime)
    pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='''python helloTop.py -e dev -s 10''')

    parser.add_argument('-e', '--env', help='env name', action='store', default="dev")
    parser.add_argument('-s', '--sleep', help='sleep time', action='store', default=0)

    args = parser.parse_args()

    env_type = args.env
    sleeptime = int(args.sleep)

    logger.info("env is %s, sleeptime is %d", env_type, sleeptime)

    start(env_type, sleeptime)