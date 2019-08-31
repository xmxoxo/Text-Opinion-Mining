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
import re
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

    #读取原句子
    print('正在读取原句')
    fndat = './data/reviews.csv'
    df_review = pd.read_csv(fndat)
    #获取所有句子
    lstReview = list(df_review['Reviews'])
    print(lstReview[:5])
    print('-'*30)
    #获得子句索引
    lstSubSeg = [getSubSeg(x) for x in lstReview]
    print(lstSubSeg[:5])
    print('-'*30)
    #-----------------------------------------
    tokenfile = os.path.join(path, 'token_test.txt')
    labelfile = os.path.join(path, 'label_test.txt')

    #读取索引信息
    txttoken = pd.read_csv(tokenfile,delimiter="\t", header = None)
    txtlbl = pd.read_csv(labelfile,delimiter="\t", header = None)

    #合并
    txtout = pd.merge(txttoken,txtlbl,left_index=True,right_index=True,how='outer')
    mergefn = os.path.join(path, 'merge_test.txt')
    txtout.to_csv(mergefn,index=False,sep="\t",header = None)
    print(txtout.head(10))   
    print('-'*30)

    #生成句子拆分标识索引号
    #2019/8/30 这里有错误，要改成统一的字段名
    f_index0 = txtout[txtout.columns[0]][txtout[txtout.columns[0]].isin(['[CLS]'])]
    f_index1 = txtout[txtout.columns[0]][txtout[txtout.columns[0]].isin(['[SEP]'])]
    lstSeg = list(zip(list(f_index0.index),list(f_index1.index)))
    print(lstSeg[:10])
    print(len(lstSeg))
    #print(lstSeg[217:220])

    #for i in range(len(lstSeg)):
    #    print('%d : %s' % (i, lstSeg[i]) )        
    #return 0
    #-----------------------------------------
    #返回索引所在的位置
    #给数据增加ID号, lstSeg 记录着每条记录的开始与结束
    #test:[(0, 39), (40, 70), (71, 86), (87, 100)]
    #train:[(0, 10), (11, 28), (29, 53), (54, 82)]
    def getid (index,lstS = lstSeg):
        for i in range(len(lstS)):
            tseg = lstS[i]
            if tseg[0]<=index<tseg[1]:
                return int(i+1)
                break
        return 0
    #-----------------------------------------
    #print(getid(5391, lstSeg) )
    #print('-'*30)
    #sys.exit()


    #提取label
    labels = ["B-ASP", "I-ASP", "B-OPI", "I-OPI"]
    fout = txtout[txtout[txtout.columns[1]].isin(labels)]
    print(fout.head(10))   
    print('-'*30)
    #if not fout:
    #    print('数据错误...')
    #    return ''
    

    #把标注数据结果提取出来，循环遍历记录
    lstid = []
    lstindex = []
    lsttxt = []
    lstlabel = []
    lstSubPos = []
    lstindex_new = []
    lstSegIndex = []

    seg = ''
    index = 0
    lastlbl = ''
    fid = 0
    subindex = 0 #当前句索引
    for x in fout.index:
        word = fout[fout.columns[0]][x]
        lbl = fout[fout.columns[1]][x]
        #ffid = getid(x)
        subindex +=1
        #跨句子
        if x > lstSeg[fid][1]:
            if seg and lastlbl:
                #print ('当前id：%d' % ffid)
                fid = getid(index)-1
                lstid.append( fid+1 )

                lstindex.append(index)
                lsttxt.append(seg)
                lstlabel.append(lastlbl[-3:])
                #计算当前句位置
                lstSegIndex.append(lstSeg[fid][0])
                #2019/8/31 注意要多减1
                indexnew = index - lstSeg[fid][0]-1
                lstindex_new.append(indexnew)
                #第几个子句
                lstSubPos.append(getid(indexnew, lstS = lstSubSeg[fid]) )
            seg = word
            index = x
            lastlbl = lbl

            fid += 1
            subindex = 0
            continue

        #2019/8/30 如果标注不连续也要进行处理，增加: or ( x - (index + len(seg)) )>1 
        if lbl[0] == 'B' or lastlbl[-3:] != lbl[-3:] or ( x - (index + len(seg)) )>1 :
            if seg and lastlbl:
                fid = getid(index)-1
                lstid.append( fid+1 )

                lstindex.append(index)
                lsttxt.append(seg)
                lstlabel.append(lastlbl[-3:])
                #计算当前句位置
                lstSegIndex.append(lstSeg[fid][0])
                #print(x,fid,lstSeg[fid])
                indexnew = index - lstSeg[fid][0]-1
                lstindex_new.append(indexnew)
                #第几个子句
                lstSubPos.append(getid(indexnew, lstS = lstSubSeg[fid]) )

            seg = word
            index = x
        else:
            seg +=word
        lastlbl = lbl

        #if x>100:
            #pass
            #break
        

    #循环结束后最后一条记录要处理
    print('最后记录')
    print(fid, seg , lastlbl, x)
    if seg and lastlbl:
        #lstid.append(fid+1)
        fid = getid(index)-1
        lstid.append( fid +1 )
        lstindex.append(x)
        lsttxt.append(seg)
        lstlabel.append(lastlbl[-3:])
        #计算当前句位置
        lstSegIndex.append(lstSeg[fid][0])
        #print(x,fid,lstSeg[fid])
        indexnew = index - lstSeg[fid][0]
        lstindex_new.append(indexnew)
        #print(indexnew)
        #第几个子句
        lstSubPos.append(getid(indexnew, lstS = lstSubSeg[fid]) )

    #转为字典
    dictDat = {
        'id':lstid,
        'index':lstindex,
        'txt':lsttxt,
        'label':lstlabel,
        'segIndex': lstSegIndex,
        'index_new':lstindex_new, #本句索引位置
        'subPos': lstSubPos, #所在分句
    }

    #转为DataFrame
    outdf = pd.DataFrame(dictDat)
    print(outdf.head(10))
    print('-'*30)
    #return 0

    #----- 2019/8/30 以下部分合并到循环中去了-----
    #outdf['id'] = outdf['index'].apply(getid)
    #outdf = outdf[['id','index','txt','label']]
    #print(outdf.head(10))
    #print('-'*30)

    #Todo: 还要把ASP和OPI进行组合下
    
    #把索引转换成本句的索引， 用索引号减去lstSeg[句子id]即可
    #outdf['index_new'] = outdf['index'].apply(lambda x: x - lstSeg[getid(x)-1][0])
    #print(outdf.head(10))
    #print('-'*30)

    #求出子句的位置，放在字段subPos；相关字段：'id':第几句，要-1；'index_new':本句位置
    #outdf['subPos'] = outdf.apply(lambda x: getid(x['index_new'], lstS=lstSubSeg[x['id']-1]), axis=1)
    #print('标识子句位置suubPos:')
    #print(outdf.head(10))
    #print('-'*30)
    #-----------------------------------------

    #存个临时数据用于分析
    outfile = os.path.join(path, 'seg_test.txt')
    outdf.to_csv(outfile,index=False)
    #return 0

    #合并最后的结果，相关字段：id：第几句，subPos：第几个子句
    #字段： id , index , txt, label , index_new , subPos
    #循环遍历所有的记录，如果ID与subPos都相同，进行拼接
    #最终结果字段： id, ASP, OPI
    lstID = []
    lstASP = []
    lstOPI = []
    lstAStar = []
    lstOStar = []
    
    cID = 0
    cSub = 0
    lastID = 0
    lastSub = 0
    lastTxt = ''
    lastLbl = ''
    txt = ''
    lbl = ''
    lastASP = ''
    lastOPI = ''
    lastAStar = ''
    lastOStar = ''
    for x in outdf.index:
        cID = outdf['id'][x]
        txt = outdf['txt'][x]
        lbl = outdf['label'][x]
        cSub = outdf['subPos'][x]
        cPos = outdf['index_new'][x]

        #判断是否同一个子句
        if cID==lastID and cSub==lastSub:
            #是同一个子句,判断填充内容
            #2019/8/30 增加特殊情况，同一个子句中连续出现同一个标签
            if (lastASP and lastOPI) or \
                (lastASP and lbl=='ASP') or (lastOPI and lbl=='OPI' ):
                if lastASP=='':lastASP = '_'
                if lastOPI=='':lastOPI = '_'
                lstID.append(lastID)
                lstASP.append(lastASP)
                lstOPI.append(lastOPI)
                lastASP = ''
                lastOPI = ''
                lstAStar.append(lastAStar)
                lstOStar.append(lastOStar)
                lastAStar = ''
                lastOStar = ''
            
        else:
            #不是同一句,之前又有数据，则先旧数据保存起来
            if lastASP or lastOPI:
                if lastASP=='':lastASP = '_'
                if lastOPI=='':lastOPI = '_'
                lstID.append(lastID)
                lstASP.append(lastASP)
                lstOPI.append(lastOPI)
                lastASP = ''
                lastOPI = ''
                lstAStar.append(lastAStar)
                lstOStar.append(lastOStar)
                lastAStar = ''
                lastOStar = ''
        
        lastID = cID
        lastTxt = txt
        lastLbl = lbl
        lastSub = cSub
        if lbl=='ASP':
            if not lastASP:
                lastASP = lastTxt
                lastAStar = cPos
        if lbl=='OPI':
            if not lastOPI:
                lastOPI = lastTxt
                lastOStar = cPos
        
        #print(lastID,lastASP,lastOPI)
        #print('-'*10)
        #if x>10:
        #    break

    #循环结果后还有结果要处理下
    if lastASP or lastOPI:
        if lastASP=='':lastASP = '_'
        if lastOPI=='':lastOPI = '_'
        lstID.append(lastID)
        lstASP.append(lastASP)
        lstOPI.append(lastOPI)
        lstAStar.append(lastAStar)
        lstOStar.append(lastOStar)

    '''
    print(lstID[:10])
    print(lstASP[:10])
    print(lstOPI[:10])
    print('-'*30)
    #return 0
    '''

    #转为字典
    dictDat = {
        'id':lstID,
        'ASP':lstASP,
        'OPI':lstOPI,
        'A_start':lstAStar,
        'O_start':lstOStar,
    }

    #转为DataFrame
    outdf = pd.DataFrame(dictDat)
    print(outdf.head(10))
    #return 0

    #保存提取的结果
    outfile =  os.path.join(path, 'picklabel_test.txt')
    outdf.to_csv(outfile,index=False) #,sep="\t"
    print('提取记录数: %d' % outdf.shape[0])
    print('提取结果保存完成: %s' % outfile)
    print('-'*30)


#把句子拆分子句，并返回各句子的起止索引号
# txt = '最近太忙一直没有空来评价，东西已试过是正品，擦在脸上勾称白嫩，是个不错的商品'
#返回结果： [(0, 13), (13, 22), (22, 31), (31, 38)]
def getSubSeg(txt):
    #2019/8/30 子句拆分优化：连续空格替换成单空格；子句分隔加入空格
    #txt = re.sub('([ ]+)',r" ",txt)
    txt = re.sub(r'([ ，；。！])',r"\1\n", txt)
    nlist = txt.splitlines()
    #print(nlist)
    lstPos = [len(x) for x in nlist]
    #print(lstPos)
    x = 0
    lstRet = []
    for i in range(len(lstPos)):
        lstRet.append( (x, x + lstPos[i]) )
        x += lstPos[i]
    return lstRet


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
    

