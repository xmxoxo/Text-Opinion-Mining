#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo'


'''
NER预测结果提取工具 

自动分析指定目录下的label_test.txt和token_test.txt，
提取出已经识别的结果，并保存到result_test.txt中

提取后的格式如下：
```
index    位置索引，从0开始
txt      文本内容
label    标签
```

提取结果样例：

```
index   txt         label
5       金庸        PER  
65      提婆达多    PER
309     帝释        PER
```

'''

import os
import sys
import pandas as pd

# 读入文件
def readtxtfile(fname):
    pass
    with open(fname,'r',encoding='utf-8') as f:  
        data=f.read()
    return data

#保存文件
def savetofile(txt,filename):
    pass
    with open(filename,'w',encoding='utf-8') as f:  
        f.write(str(txt))
    return 1



#主方法
def doprocess(path):
    labels = ["B-ASP", "I-ASP", "B-OPI", "I-OPI"]
    tokenfile = os.path.join(path, 'token_test.txt')
    labelfile = os.path.join(path, 'label_test.txt')

    #读取索引信息
    txttoken = pd.read_csv(tokenfile,delimiter="\t", header = None)
    txtlbl = pd.read_csv(labelfile,delimiter="\t", header = None)

    #合并
    txtout = pd.merge(txttoken,txtlbl,left_index=True,right_index=True,how='outer')
    mergefn = os.path.join(path, 'merge_test.txt')
    txtout.to_csv(mergefn,index=False,sep="\t",header = None)

    fout = txtout[txtout[txtout.columns[1]].isin(labels)]
    print(fout.head(10))   
    print('-'*30)

    #把数据提取出来
    lstindex = []
    lsttxt = []
    lstlabel = []

    seg = ''
    index = 0
    for x in fout.index:
        word = fout[fout.columns[0]][x]
        lbl = fout[fout.columns[1]][x]
        
        #print(word,lbl)
        #break
        if lbl[0] == 'B':
            if len(seg)>1:
                lstindex.append(index)
                lsttxt.append(seg)
                lstlabel.append(lbl[-3:])
            seg = word
            index = x
        else:
            seg +=word

    '''
    print(lstindex[:20])
    print(lsttxt[:20])
    print(lstlabel[:20])
    print('-'*30)
    '''
    
    #转为字典
    dictDat = {
        'index':lstindex,
        'txt':lsttxt,
        'label':lstlabel,
    }

    #转为DataFrame
    outdf = pd.DataFrame(dictDat)
    print(outdf.head(10))

    #保存提取的结果
    outfile =  os.path.join(path, 'picklabel_test.txt')
    outdf.to_csv(outfile,index=False,sep="\t")
    print('result saved!')
    print('-'*30)

    #筛选
    #print(outdf.mean())
    
    '''
    #分组
    gp = outdf[outdf.columns[1]]
    #print(gp.columns())
    gp = gp.sort_values(0)
    #print(gp)

    result= pd.value_counts(gp)
    #print(result)
    print(result.head(20))
    #outdf.groupby(outdf.columns[0])
    #print(outdf.head(25))
    #savetofile (str(result) , os.path.join(path, 'label_count.txt'))
    result.to_csv(os.path.join(path, 'label_count.txt'),sep="\t")
    '''

#命令行方法
def maincli ():
    pass
    path = './output/'
    if len(sys.argv)>1:
        path = sys.argv[1]
    
    #print('目录:%s' % path)
    if not os.path.exists(path):
        print('目录%s不存在，请检查!' % path)
        sys.exit(0)
    
    doprocess(path)


if __name__ == '__main__':
    pass
    maincli()
    

