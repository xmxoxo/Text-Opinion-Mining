#!/usr/bin/env python3
#coding:utf-8
# update : 2019/8/30 8:31
# version: 0.2.0
__author__ = 'xmxoxo<xmxoxo@qq.com>'

'''
模型评价工具 modelscore.py

电商评论观点挖掘 比赛 https://zhejianglab.aliyun.com/entrance/231731/introduction
四、评分标准
1、相同ID内逐一匹配各四元组，若AspectTerm，OpinionTerm，Category，Polarity四个字段均正确，则该四元组正确；
2、预测的四元组总个数记为P；真实标注的四元组总个数记为G；正确的四元组个数记为S：
（1）精确率： Precision=S/P
（2）召回率： Recall=S/G
（3）F值:F1-score=(2*Precision*Recall)/(Precision+Recall)

命令行格式:
python modelscore.py -h
python modelscore.py 原始数据文件 预测结果文件

参数说明：
    原始数据文件: 原始数据文件，默认为 ./TRAIN/Train_labels.csv
    预测结果文件：模型预测输出的结果文件，默认值为 ./output/Result.csv

快速进行评价： python modelscore.py
指定文件评价： python modelscore.py ./data/labels.csv ./output1/Result.csv

'''

import os
import sys
import pandas as pd
import argparse


#计算得分
def getscore (lstS,lstP):
    y_test = list(lstS)
    classs_predictions = list(lstP)
    ret = ""

    #预测的四元组总个数记为P
    P = len(classs_predictions)
    #真实标注的四元组总个数记为G；
    G = len(y_test)
    #1、相同ID内逐一匹配各四元组，若AspectTerm，OpinionTerm，Category，Polarity四个字段均正确，则该四元组正确；
    #正确的四元组个数记为S：
    S = 0
    setRet = set()
    for x in classs_predictions:
        if x in y_test:
    #for x in y_test:
    #    if x in classs_predictions:
            setRet.add(x)
            S += 1
    S1 = len(setRet)
    ret += '唯一正确：%d, 正确个数:%d\n' % (S1,S)
    S = S1
    #print('P:%d G:%d S:%d' %  (P,G,S) )
    ret += 'P:%d G:%d S:%d\n' %  (P,G,S)

    if P == 0:
        Precision,Recall,f1_score = 0,0,0
    else:
        #（1）精确率： Precision=S/P
        Precision = S/P
        #（2）召回率： Recall=S/G
        Recall = S/G
        #（3）F值:F1-score=(2*Precision*Recall)/(Precision+Recall)
        f1_score = (2*Precision*Recall)/(Precision+Recall)

    ret += "精确率: %2.3f\n" % ( Precision)
    ret += "召回率: %2.3f\n" % ( Recall)
    ret += "F1得分: %2.3f\n" % ( f1_score) 
    return ret
#-----------------------------------------


#主方法 模型评估
def modelscore (args):
    sorucefile = args.soruce
    predictfile = args.result
    if not os.path.isfile(sorucefile):
        print('未找到原始数据文件:%s' % sorucefile )
        sys.exit()

    if not os.path.isfile(predictfile):
        print('未找到预测结果文件:%s' % predictfile )
        sys.exit()


    #读入数据
    df_source = pd.read_csv(sorucefile)
    df_predict = pd.read_csv(predictfile,header = None)
    #字段处理
    #id,AspectTerms,A_start,A_end,OpinionTerms,O_start,O_end,Categories,Polarities
    lstColumns = ['id','AspectTerms','OpinionTerms','Categories','Polarities']
    df_source = df_source[lstColumns]
    df_predict.columns = lstColumns
    
    #2019/8/30 todo: 加入数据分析

    #把各字段文本连接起来
    df_source['txt'] = df_source['id'].astype(str) + df_source['AspectTerms'] + \
        df_source['OpinionTerms']+df_source['Categories']+df_source['Polarities']

    df_predict['txt'] = df_predict['id'].astype(str) + df_predict['AspectTerms'] + \
        df_predict['OpinionTerms']+df_predict['Categories']+df_predict['Polarities']

    #把各字段文本连接起来
    df_source['txt1'] = df_source['id'].astype(str) + \
            df_source['AspectTerms'] + df_source['OpinionTerms']

    df_predict['txt1'] = df_predict['id'].astype(str) + \
            df_predict['AspectTerms'] + df_predict['OpinionTerms']

    print('数据记录情况'.center(30,'=')) # + '\n'
    print(df_source.head(10))
    print('-'*30)
    print(df_predict.head(10))
    print('-'*30)

    ret = ""
    ret += '抽取模型评估得分'.center(30,'=') + '\n'
    ret +=  getscore (df_source['txt1'],df_predict['txt1'] )
    ret += '完整模型评估得分'.center(30,'=') + '\n'
    ret +=  getscore (df_source['txt'],df_predict['txt'] )

    print(ret)
    print('-'*30)


#命令行解析 
def main_cli ():
    pass
    parser = argparse.ArgumentParser(description='“电商评论观点挖掘”比赛模型评价，计算模型各项得分')
    parser.add_argument('-soruce', type=str, default="./TRAIN/Train_labels.csv",
                        help='原始数据文件，默认为 ./TRAIN/Train_labels.csv')
    parser.add_argument('-result', type=str, default='./output/Result.csv',
                        help='预测结果文件，默认为 ./output/Result.csv')
    args = parser.parse_args()
    modelscore(args)

if __name__ == '__main__':
    pass
    main_cli()
