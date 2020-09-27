数据存储到`top_data` 集合之后，可以执行下面的语句，来统计总的次数、总的耗时，哪个时间段，读次数最多，是多少等等


```
db.top_data.group({
    key: { collectionName: 1 },
    initial: {
        totalCount: 0,
        totalCost: 0,
        readCount: 0,
        readTime: 0,
        writeCount: 0,
        writeTime: 0,

        maxReadCount: 0,
        maxReadCountTime: "",
        maxReadCost: 0,
        maxReadCostTime: "",

        maxWriteCount: 0,
        maxWriteCountTime: "",
        maxWriteCost: 0,
        maxWriteCostTime: ""
    },
    reduce: function(doc, out){
        out.totalCount += doc.totalCount;
        out.totalCost += doc.totalTime;

        out.readCount += doc.readCount;
        out.readTime += doc.readTime;

        out.writeCount += doc.writeCount;
        out.writeTime += doc.writeTime;

        var isMax = false;
        isMax = doc.readCount > out.maxReadCount;
        out.maxReadCount = isMax ? doc.readCount : out.maxReadCount;
        out.maxReadCountTime = isMax ? doc.createTime : out.maxReadCountTime;

        isMax = doc.readTime > out.maxReadCost;
        out.maxReadCost = isMax ? doc.readTime : out.maxReadCost;
        out.maxReadCostTime = isMax ? doc.createTime : out.maxReadCostTime;

        isMax = doc.writeCount > out.maxWriteCount;
        out.maxWriteCount = isMax ? doc.writeCount : out.maxWriteCount;
        out.maxWriteCountTime = isMax ? doc.createTime : out.maxWriteCountTime;

        isMax = doc.writeTime > out.maxWriteCost;
        out.maxWriteCost = isMax ? doc.writeTime : out.maxWriteCost;
        out.maxWriteCostTime = isMax ? doc.createTime : out.maxWriteCostTime;
  }
})
```