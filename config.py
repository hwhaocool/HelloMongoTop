#coding:utf-8

import simplejson
import re

class MyConfig:

    __json = None

    def __init__(self):
        """构造方法"""
        f = open("config.json", "r")

        self.__json = simplejson.load(f)
        f.close()

    def get(self, key):
        ''''''
        return self.__json[key]

if __name__ == '__main__':
    s = MyConfig()
    print(s.get("dev"))