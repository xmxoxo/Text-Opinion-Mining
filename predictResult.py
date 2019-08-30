#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

'''
分类模型预测结果格式化都是一样的，只要把预测结果中每行中的最大值索引取出，对应到标签即可；

程序文件名： predictResult.py
需要的参数：
	测试文件 ./data/test.tsv; 
	标签字典, ./output/label2id.pkl
	预测结果, ./output/test_results.tsv (注意：编码是936)

输出结果文件：./output/predict.csv
'''
import os
import sys
import pandas as pd
import pickle


#分类模型预测结果格式化
def formatPerdict (testfile , labelfile , predictfile, outfile):
    pass
    #读取标签字典
    print('正在读取标签字典...')
    label2id={}
    if os.path.exists(labelfile):
        with open(labelfile, 'rb') as rf:
            label2id = pickle.load(rf)
            id2label = {value: key for key, value in label2id.items()}
            #print(label2id)
            #print(id2label)
    else:
        print('标签字典读取失败...')
        return 0
    #读取预测结果
    df = pd.read_csv(predictfile, header = None,sep = '\t', encoding = 'gb2312')
    print(df.head())
    #求最大值及最大值索引号
    df_n = pd.DataFrame()
    df_n['max_idx']=df.idxmax(axis=1)
    df_n['max_val']=df.max(axis=1)
    df_n['label']= df_n['max_idx'].apply(lambda x: id2label[x])
    print(df_n.head())
    #保存结果
    df_ret = df_n[['label']]
    df_ret.to_csv(outfile, index = False)
    print('分类结果格式化完成:%s ' % outfile)

#命令行方法
def maincli ():
    pass
    path = './'
    if len(sys.argv)>1:
        path = sys.argv[1]
    
    #print('目录:%s' % path)
    if not os.path.exists(path):
        print('目录%s不存在，请检查!' % path)
        sys.exit(0)

    lstFiles = ['data/test.tsv',
        'output/label2id.pkl',
        'output/test_results.tsv',
        'output/predict.csv',
        ]

    testfile , labelfile , predictfile, outfile = [os.path.join(path,x) for x in lstFiles]
    
    #print(testfile , labelfile , predictfile, outfile)

    formatPerdict(testfile , labelfile , predictfile, outfile)


if __name__ == '__main__':
    pass
    maincli()

