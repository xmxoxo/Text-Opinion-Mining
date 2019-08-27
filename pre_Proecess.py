#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

import os
import sys
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

from datetime import datetime

path= './train/'

#数据预处理

# 读入文件
def readtxtfile(fname,encoding='utf-8'):
    pass
    try:
        with open(fname,'r',encoding=encoding) as f:  
            data=f.read()
        return data
    except :
        return ''


#保存文本信息到文件
def savetofile(txt,filename,encoding='utf-8'):
    pass
    try:
        with open(filename,'w',encoding=encoding) as f:  
            f.write(str(txt))
        return 1
    except :
        return 0

##指定列按特征索引值进行映射到新列newColumn
def MapNewColumn(df,oldcol,newcol,isdrop  = 1):
    pass
    A = df[oldcol].value_counts().argsort()
    print('[%s]列值分布情况:' % oldcol)
    # ----- 要把映射后的值 保存下来下次用；-----
    print(A)
    #print(type(A))
    dict_oldcol = {'index':A.index,'values':A.values}
    df_oldcol = pd.DataFrame(dict_oldcol)
    df_oldcol.to_csv('./MapNewColumn_%s.csv' % oldcol )
    print('[%s]列值分布情况已保存' % oldcol)
    # -----
    df[newcol] = df[oldcol].map(A)
    if isdrop:
        df.drop(oldcol,axis=1, inplace=True)
    #2019.3.27 做one-hot
    #df = MakeDummies(df,newcol)
    return df

#指定列按特征索引值进行映射到新列newColumn
#如果未指定文件名，则根据列名自动加载映射文件
def pre_MapNewColumn(df,oldcol,newcol, mapfile = ''):
    try:
        if not mapfile:
            mapfile = 'MapNewColumn_%s.csv' % oldcol
        print('正在载入字典文件:%s...' % mapfile)
        dfkey = pd.read_csv(mapfile,index_col=[0])
        dictKey = dfkey.set_index('index').T.to_dict('records')[0]
        #print(dictKey)
        df[newcol] = df[oldcol].map(dictKey)
        df.drop(oldcol,axis=1, inplace=True)
        return df
    except Exception as e:
        logging.error('Error : '+ traceback.format_exc())
        #print(e)
        return None    

#数据字段处理：从字段列表文件中读取字段清单，并进行重新选择
def pre_FixColumns (df, filename = 'datColumns.txt'):
    try:
        if not filename:
            filename = 'datColumns.txt'
        strTxt = readtxtfile(filename,encoding='gb2312')
        if strTxt:
            lstColumns = strTxt.split('\n')
            df = df[lstColumns]
        return df
    except Exception as e:
        logging.error('Error : '+ traceback.format_exc())
        return df

#把原文内容合并到四元组记录中，形成新的数据文件
def DatMerge (path= './train/', rebuild = 0):
    fnout = os.path.join(path, 'Train_merge.csv')
    if rebuild:
        print('指定强制重新生成数据文件...')
    else:
        if os.path.isfile(fnout):
            print('数据文件已生成,跳过生成步骤...')
            return 0
    
    fn1 = os.path.join(path, 'Train_reviews.csv')
    fn2 = os.path.join(path, 'Train_labels.csv')
    
    df1 = pd.read_csv(fn1)
    df2 = pd.read_csv(fn2)
    
    print(df1.info())
    print(df1.shape)
    
    print(df2.info())
    print(df2.shape)
    
    print(df1['Reviews'][df1['id']==35])
    print(df1.iloc[35]['Reviews'] )
    def getText(x):
        #return df1['Reviews'][df1['id']==int(x)]
        return df1.iloc[x-1]['Reviews']
        
    df2['text'] = ''
    df2['text'] = df2['id'].apply(getText)
    print(df2.head(10))
    #save 
    df2.to_csv(fnout)

#统计所有的 种类 Categories 和 极性Polarities 的值 
def getEnum (path= './train/'):
    fnout = os.path.join(path, 'Train_merge.csv')
    df = pd.read_csv(fnout,index_col=[0])

    df = MapNewColumn(df,'Categories','Categories_v')
    df = MapNewColumn(df,'Polarities','Polarities_v')

#生成序列标注训练文件
def CreateSerialFile (path= './train/', rebuild = 0):
    pass
    fnout = os.path.join(path, 'train.txt') 
    if rebuild:
        print('指定强制重新生成标注文件...')
    else:
        if os.path.isfile(fnout):
            print('标注文件已生成,跳过生成步骤...')
            return 0

    
    fndat = os.path.join(path, 'Train_merge.csv')
    df = pd.read_csv(fndat,index_col=[0])

    strTxt = ''
    lastId = ''
    strLine = ''
    lstLine = []
    print('正在生成标注文件...')
    #循环处理每一行
    #字段列表： id,AspectTerms,A_start,A_end,OpinionTerms,O_start,O_end
    for i in range(len(df)):
        pass
        x = df.iloc[i]
        sid = x['id']
        #不同的ID出现时，把上一个值保存起来
        if lastId!=sid:
            if lstLine:
                strTxt += '\n'.join(lstLine)+'\n\n'
            
            lastId=sid
            strLine = x['text']
            #去掉*号
            #strLine = strLine.replace('*','')

            lstLine = [ x+' O' for x in list(strLine)]  
        
        if x['AspectTerms']!='_':
            for j in range(int(x['A_start']), int(x['A_end'])):
                if i==x['A_start']: 
                    lstLine[j]= lstLine[j].replace(' O',' B-ASP')
                else:
                    lstLine[j]= lstLine[j].replace(' O',' I-ASP')
        if x['OpinionTerms']!='_':
            for j in range(int(x['O_start']), int(x['O_end'])):
                if i==x['A_start']: 
                    lstLine[j]= lstLine[j].replace(' O',' B-OPI')
                else:
                    lstLine[j]= lstLine[j].replace(' O',' I-OPI')
             
        #if i>10:
        #    print(strTxt)
        #    break
    #保存
    savetofile(strTxt, fnout)
    print('标注数据已保存。')
    

if __name__ == '__main__':
    pass
    #合并数据
    DatMerge()
    #getEnum()

    #生成序列标注文件
    CreateSerialFile()
