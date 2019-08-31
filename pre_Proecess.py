#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

#数据预处理
import re
import os
import sys
import pandas as pd
import numpy as np
import time
import argparse

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

#把原文内容合并到四元组记录中，形成新的数据文件
def DatMerge (fn1 = './TRAIN/Train_reviews.csv', fn2 = './TRAIN/Train_labels.csv', \
            fnout = './data/Train_merge.csv', rebuild = 0):
    
    #fnout = os.path.join(outpath, 'Train_merge.csv')
    if rebuild:
        print('指定强制重新生成数据文件...')
    else:
        if os.path.isfile(fnout):
            print('数据文件已生成,跳过生成步骤...')
            return 0
    
    #fn1 = os.path.join(path, 'Train_reviews.csv')
    #fn2 = os.path.join(path, 'Train_labels.csv')
    df1 = pd.read_csv(fn1)
    df2 = pd.read_csv(fn2)

    '''
    print(df1.info())
    print(df1.shape)
    
    print(df2.info())
    print(df2.shape)
    '''
    
    #print(df1['Reviews'][df1['id']==35])
    #print(df1.iloc[35]['Reviews'] )
    def getText(x):
        #return df1['Reviews'][df1['id']==int(x)]
        return df1.iloc[x-1]['Reviews']

            
    df2['text'] = ''
    df2['text'] = df2['id'].apply(getText)
    print('数据合并结果：')
    print(df2.head(10))
    print('-'*30)
    #save 
    df2.to_csv(fnout)

#统计所有的 属性分类 Categories 和 观点分类 Polarities 的值 
def getEnum (path= './TRAIN/',rebuild = 0):
    fnout = os.path.join(path, 'Train_merge.csv')
    df = pd.read_csv(fnout,index_col=[0])

    df = MapNewColumn(df,'Categories','Categories_v')
    df = MapNewColumn(df,'Polarities','Polarities_v')

##给数据增加ID号, lstSeg 记录着每条记录的开始与结束
    #test:[(0, 39), (40, 70), (71, 86), (87, 100)]
    #train:[(0, 10), (11, 28), (29, 53), (54, 82)]
def getid (index,lstS):
    for i in range(len(lstS)):
        tseg = lstS[i]
        if tseg[0]<=int(index)<tseg[1]:
            # print(tseg)
            return tseg
            # return int(i+1)
            break

def getSubSeg(txt):
    #2019/8/30 子句拆分优化：连续空格替换成单空格；子句分隔加入空格
    # txt = re.sub('([  ]+)',r" ",txt)
    txt = re.sub(r'([ ，；。！])',r"\1\n", txt)
    nlist = txt.splitlines()
    # print(nlist)
    lstPos = [len(x) for x in nlist]
    #print(lstPos)
    x = 0
    lstRet = []
    for i in range(len(lstPos)):
        lstRet.append( (x, x + lstPos[i]) )
        x += lstPos[i]
    # print(lstRet)
    return lstRet

#生成序列标注训练文件
def CreateSerialFile (path= './TRAIN/', outpath = './data/' , rebuild = 0):
    pass
    fnout = os.path.join(outpath, 'train.txt') 
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
    #Todo:  训练集:验证集 比例 = 8:2 （按记录条数）

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
            #是否去掉一些特殊符号，注意去掉符号可能影响索引位置
            #特殊符号有： &thinsp ** ?? 等
            #strLine = strLine.replace('*','')

            lstLine = [ x+' O' for x in list(strLine)]  
        
        if x['AspectTerms']!='_':
            for j in range(int(x['A_start']), int(x['A_end'])):
                if str(j)==x['A_start']: 
                    lstLine[j]= lstLine[j].replace(' O',' B-ASP')
                else:
                    lstLine[j]= lstLine[j].replace(' O',' I-ASP')
        if x['OpinionTerms']!='_':
            for j in range(int(x['O_start']), int(x['O_end'])):
                if str(j)==x['O_start']: 
                    lstLine[j]= lstLine[j].replace(' O',' B-OPI')
                else:
                    lstLine[j]= lstLine[j].replace(' O',' I-OPI')
             
        #if i>10:
        #    print(strTxt)
        #    break
    #2019/8/30 补充最后一句
    if lstLine:
        strTxt += '\n'.join(lstLine)+'\n\n'

    #保存数据
    #print(strTxt[-40:] )
    savetofile(strTxt+'\n\n', fnout)
    print('标注数据已保存。')
    
#生成标注测试集的数据样本
#原始文件：./data/reviews.csv  需要把等预测的数据复制到这里
#目标文件：./data/test.txt
def CreateTestSet (sourcefile = './data/reviews.csv', outpath = './data/', rebuild = 0):
    pass
    fnout = os.path.join(outpath, 'test.txt')
    if rebuild:
        print('重新生成测试集文件...')
    else:
        if os.path.isfile(fnout):
            print('测试集数据文件已生成,跳过生成步骤...')
            return 0

    print('正在生成测试集文件...')
    #读取数据文件
    #fn = os.path.join(path, 'reviews.csv')
    df = pd.read_csv(sourcefile)
    #print(df.shape)
    #字段列表： id,Reviews
    sTxt = '\n'.join(list(df['Reviews']))
    #print('-'*30)
    #print(sTxt[-100:] )
    #print('-'*30)
    #return 0
    strRet = '\n'.join([ x + ' O' if x!='\n' else '' for x in sTxt])
    print('-'*30)
    print( strRet[:40] + '\n...\n' + strRet[-40:] )
    print('-'*30)
    #坑：结束要加两个换行，不然会漏数据 2019/8/28 
    savetofile(strRet + '\n\n', fnout)
    print('测试集标注数据已生成。')


def myfunction(a,b,txt):
    '''
    a = str(a).strip() + ''
    b = str(b).strip() + ''
    pos = a if a !='' else b
    #print('pos=', pos)
    pos = int(pos)
    '''

    #print('-'*30)
    #print(a,b,txt)
    pos = a if a >=0 else b
    #print(pos)

    lstRet = getSubSeg(txt)
    #print(lstRet)
    tseg = getid(pos, lstRet)
    #print(tseg)
    t = txt[tseg[0]:tseg[1]]
    # print(t)
    return t

#生成观点分类模型训练数据
#字段列表：,id,AspectTerms,A_start,A_end,OpinionTerms,O_start,O_end,Categories,Polarities,text
def CreatePolarityTrain (path= './TRAIN/', outpath = './Polarity/data/', rebuild = 0):
    pass
    fnout = os.path.join(outpath, 'train.tsv') 
    if rebuild:
        print('指定强制重新生成 观点分类模型训练数据文件...')
    else:
        if os.path.isfile(fnout):
            print('观点分类训练文件已生成,跳过生成步骤...')
            return 0
    
    fndat = os.path.join(path, 'Train_merge.csv')
    df = pd.read_csv(fndat,index_col=[0])
    
    #df = MapNewColumn(df,'Polarities','label')
    '''
    [Polarities]列值分布情况:
    正面    2
    负面    1
    中性    0
    Name: Polarities, dtype: int64
    '''
    #lstLabels = ['正面','中性','负面']
    #df['label'] = df['Polarities'].apply(lambda x: lstLabels.index(x))
    #print(df.head(10))
    df = df.replace(' ',np.nan)
    df = df.fillna(-1)
    print(df.head(10))

    df['new_text'] = df.apply(lambda x: myfunction(x.A_start,x.O_start,x.text),axis=1)


    #替换掉"_"
    # df['AspectTerms'] = df['AspectTerms'].replace('_','')
    # df['OpinionTerms'] = df['OpinionTerms'].replace('_','')
    # df['text'] = df['AspectTerms'] + df['OpinionTerms']
    #
    # #输出字段清单: Polarities,text
    dfn = df[['Polarities','new_text']]
    # #删除完全相同的数据行
    dfn = dfn.drop_duplicates()#keep='first', inplace=True)
    #
    # #数据随机打乱
    dfn = dfn.sample(frac=1)
    #
    # #数据集切分: train:dev:test = 8:2:10
    intTotal = dfn.shape[0]
    intCut = int(intTotal*0.8)
    df_train = dfn.head(intCut)
    df_dev = dfn.tail(intTotal - intCut)
    #
    # #保存数据  #,sep='\t'
    df_train.to_csv(fnout,index=False)
    df_dev.to_csv(os.path.join(outpath, 'dev.tsv'),index=False)
    dfn.to_csv(os.path.join(outpath, 'test.tsv'),index=False)
    print('观点分类模型训练数据已生成。')

#观点分类 测试数据生成
def CreatePolarityTest(path= './data/', outpath = './Polarity/data/', rebuild = 1):
    pass
    print('观点分类 测试数据生成', rebuild)
    fnout = os.path.join(outpath, 'test.tsv') 
    if rebuild:
        print('指定强制重新生成 观点分类 测试数据...')
    else:
        if os.path.isfile(fnout):
            print('观点分类测试文件已生成,跳过生成步骤...')
            return 0


    #生成合并文件
    f1 = './data/reviews.csv'
    f2 = './output/picklabel_test.txt'
    f3 = './data/data_merge.csv'
    DatMerge(f1,f2,f3,rebuild = 1)

    #f3就是要加载进来处理的文件
    #处理数据 
    df = pd.read_csv(f3,index_col=[0])#
    #df['A_Star'].astype(int)
    #df['O_Star'].astype(int)
    df.fillna(-1,inplace = True)
    #print(df.head(10)) 

    df['new_text'] = df.apply(lambda x: myfunction(x.A_start,x.O_start,x.text),axis=1)
    print(df.head(10)) 
    print('-'*30)

    #输出字段清单: Polarities,text
    dfn = df[['new_text']].copy()
    dfn['Polarities'] = '0'
    dfn = dfn[['Polarities','new_text']]

    print(dfn.head(10))
    print('-'*30)
    #sys.exit()

    #保存数据 
    dfn.to_csv(fnout,index=False)
    print('观点分类模型 测试数据已生成。')



##生成属性分类模型训练数据
def CreateCategoryTrain (path= './TRAIN/', outpath = './Category/data/', rebuild = 0):
    pass
    fnout = os.path.join(outpath, 'train.tsv') 
    if rebuild:
        print('指定强制重新生成标注文件...')
    else:
        if os.path.isfile(fnout):
            print('属性分类训练文件已生成,跳过生成步骤...')
            return 0
    
    fndat = os.path.join(path, 'Train_merge.csv')
    df = pd.read_csv(fndat,index_col=[0])

    #替换掉"_"
    df['AspectTerms'] = df['AspectTerms'].replace('_','')
    df['OpinionTerms'] = df['OpinionTerms'].replace('_','')
    df['text'] = df['AspectTerms'] + df['OpinionTerms'] 
    #df = df.fillna(-1)
    #df['new_text'] = df.apply(lambda x: myfunction(x.A_start, x.O_start, x.text), axis=1)
    
    #输出字段清单: label,text
    dfn = df[['Categories','new_text']]
    
    #删除完全相同的数据行
    dfn = dfn.drop_duplicates()#keep='first', inplace=True)

    #数据随机打乱
    dfn = dfn.sample(frac=1)
    
    #数据集切分: train:dev:test = 8:2:10
    intTotal = dfn.shape[0]
    intCut = int(intTotal*0.8)
    df_train = dfn.head(intCut)
    df_dev = dfn.tail(intTotal - intCut)

    #保存数据  #,sep='\t'
    df_train.to_csv(fnout,index=False)
    df_dev.to_csv(os.path.join(outpath, 'dev.tsv'),index=False) 
    dfn.to_csv(os.path.join(outpath, 'test.tsv'),index=False)
    print('属性分类模型训练数据已生成。')


def main_cli ():
    pass
    parser = argparse.ArgumentParser(description='数据预处理，包含训练数据与预测数据的预处理。')
    parser.add_argument('-rebuild', type=int, default="1",
                        help='强制重生成所有训练数据，默认1')
    parser.add_argument('-predictfile', type=str, default="./data/reviews.csv",
                        help='待预测文件，默认‘./data/reviews.csv’')
    parser.add_argument('-model', type=int, default="1",
                        help='运行模式,1=训练数据 0=测试数据，默认1')
    args = parser.parse_args()

    rebuild = args.rebuild
    predictfile = args.predictfile
    model = args.model 

    if model==1 :
        #----训练数据部分----

        #合并数据
        DatMerge(rebuild = rebuild)
        #生成字典
        getEnum(rebuild = rebuild)

        #训练集与验证集：生成序列标注文件
        CreateSerialFile(rebuild = rebuild)
        #观点分类训练数据生成
        CreatePolarityTrain(rebuild = rebuild)

        #属性分类模型训练数据生成
        CreateCategoryTrain(rebuild = rebuild)
        #----训练部分结束----
    else:
        #----测试数据部分----
        #生成序列标注 测试集
        CreateTestSet(sourcefile = predictfile, rebuild = rebuild)

        #观点分类 测试数据生成
        CreatePolarityTest(rebuild = rebuild)
        
        #属性分类模型 测试数据生成
        #CreateCategoryTest(rebuild = rebuild)
        #----测试部分结束----

if __name__ == '__main__':
    pass
    main_cli()