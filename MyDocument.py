#coding:utf-8

class MyDocument:

    __database = None
    __collectionName = None
    __createTime = None
    __totalTime = None
    __totalCount = None
    __readTime = None
    __readCount = None
    __writeTime = None
    __writeCount = None

    def __init__(self, database, collectionName, json_obj, createTime):
        """构造方法"""
        self.__database = database
        self.__collectionName = collectionName
        self.__createTime = createTime

        self.__totalTime = json_obj["total"]["time"]
        self.__totalCount = json_obj["total"]["count"]
        self.__readTime = json_obj["read"]["time"]
        self.__readCount = json_obj["read"]["count"]
        self.__writeTime = json_obj["write"]["time"]
        self.__writeCount = json_obj["write"]["count"]

    def getJson(self):
        '''生成可以用来插入数据库的json 对象'''
        my_json = {
            "database": self.__database,
            "collectionName": self.__collectionName,
            "createTime": self.__createTime,
            "totalTime": self.__totalTime ,
            "totalCount": self.__totalCount,
            "readTime": self.__readTime ,
            "readCount": self.__readCount ,
            "writeTime": self.__writeTime ,
            "writeCount": self.__writeCount
        }
        return my_json

if __name__ == '__main__':
    json_obj = {
        "total": {
            "time": 0,
            "count": 2
        },
        "read": {
            "time": 0,
            "count": 2
        },
        "write": {
            "time": 0,
            "count": 0
        }
    }
    document = MyDocument("xxx", "xxxx", json_obj, "2018-10-07T16:30:18.110860447+08:00")
    print str(document.getJson())