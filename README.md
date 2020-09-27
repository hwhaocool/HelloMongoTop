HelloMongoTop
---

## 功能：
循环执行`mongotop`得到结果，并把结果存到数据库中，供后续分析  
主要是用来进行数据库优化的

## 用法
```
python helloTop.py -e prod -s 20
```

`-e prod` 是指定连接哪个环境的数据库  
`-s 20` 是指定`mongotop` 运行的间隔时间，时间不要太小，不然数据会过多

如果想后台运行的话，执行`start.sh`就可以了，记得调整里面的参数哦

## config
因为安全问题，`config.json` 里面的内容被我清掉了，使用的时候记得修改

配置项解释
`host` 给`mongotop`命令行用的，注意`replicaSet`参数在开头
`dbUri` 数据保存到数据库时用的，注意`replicaSet`参数在末尾
`database` 数据写到哪个库中
`collection` 数据写到哪个集合（表）中
`sleeptime` `mongotop`采集间隔时间

## data
保存到数据中的数据如下所示
![data]( https://github.com/hwhaocool/HelloMongoTop/raw/master/picture/data_20181007201043.png )

分析结果如下所示
![analysis result](https://github.com/hwhaocool/HelloMongoTop/raw/master/picture/ana_20181007201139.png)

## 分析
需要分析的话，脚本在 `top_count.md` 里

