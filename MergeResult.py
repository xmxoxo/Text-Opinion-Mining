#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'


'''
合并所有预测数据


'''

import os
import sys
import pandas as pd
import pickle


#合并三个预测结果
#==>/output/picklabel_test.txt
#/Category/output/predict.csv
#/Polarity/output/predict.csv
#保存到/output/

def MergeDat ():
    picklabel_test = './output/picklabel_test.txt'
    Cat = './Category/output/predict.csv'
    Pol = './Polarity/output/predict.csv'
    outfile = './output/Result.csv'

    df_pick = pd.read_csv(picklabel_test)

    df_cat = pd.read_csv(Cat)
    df_pol = pd.read_csv(Pol)

    #合并 Categories,Polarities
    df_pick['Category'] = df_cat['label']
    df_pick['Polarity'] = df_pol['label']
    print(df_pick.head(10))
    print('-'*30)
    #原字段： id,ASP,OPI,A_start,O_start

    df_pick = df_pick[['id','ASP','OPI','Category','Polarity']]
    lstColumns = ['id','AspectTerms','OpinionTerms','Categories','Polarities']
    df_pick.columns = lstColumns

    #字段:['id','AspectTerms','OpinionTerms','Categories','Polarities']     
    #2019/8/29 补充id缺失的记录
    lstLost = getLost(list(df_pick['id']))
    if lstLost:
        print('正在补充缺失ID的记录...')
        #生成空记录
        lstB = list('_'*len(lstLost))
        dictDat = {
            'id':lstLost,
            'AspectTerms':lstB,
            'OpinionTerms':lstB,
            'Categories':lstB,
            'Polarities':lstB,
        }
        df_new = pd.DataFrame(dictDat)
        #接到原数据后面
        df_pick = pd.concat([df_pick,df_new], axis = 0, ignore_index= True, sort=False)
        #重新排序
        df_pick.sort_values(by=["id"],inplace= True)
    
    df_pick['id'] = df_pick['id'].astype(int)
    print(df_pick.head(10))
    print('-'*30)
    lstLost = getLost(list(df_pick['id']))
    iMax = max(list(df_pick['id']))
    print('总条数：%d, 最大ID：%d, 缺失ID数：%d' % ( df_pick.shape[0] ,iMax, len(lstLost)) )

    #保存结果
    df_pick.to_csv(outfile,index=False,header = None, line_terminator = sysCRLF() )
    print('最终结果已经保存:%s' % outfile)

#根据系统返回换行符
def sysCRLF ():
    if os.name == 'nt':
        strCRLF = '\n'
    else:
        strCRLF = '\r\n'
    return strCRLF


#获取缺失的值
#[61, 116, 139, 157, 170, 234]
def getLost(b):
    ret = []
    b = list(sorted(set(b)))
    for i in range(1,b[-1]+1): 
        if not i in b: ret.append(i)
    return ret

#命令行方法
def maincli ():
    pass
    MergeDat()

if __name__ == '__main__':
    pass

    maincli()
