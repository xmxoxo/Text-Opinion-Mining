#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

'''
预测全流程文件
使用命令行：
python run_Predict.py rebuild IsDebug
参数：  
    rebuild 强制生成数据，默认0
    IsDebug 调试模式，每步都等确认；默认0

快速预测：python run_Predict.py
重生成数据并预测：python run_Predict.py 1
调试模式预测：python run_Predict.py 1 1
'''

import os
import sys
import argparse

#2019/8/30 改为使用 argparse 控制命令行参数
parser = argparse.ArgumentParser(description='数据预处理，包含训练数据与预测数据的预处理。')
parser.add_argument('-predict', type=int, default="0",
                    help='预测数据选择，0=测试数据，1=训练数据； 默认0')
parser.add_argument('-rebuild', type=int, default="0",
                    help='强制重生成所有训练数据，默认0')
parser.add_argument('-debug', type=int, default="0",
                    help='调试模式，每步都等确认；默认0')
args = parser.parse_args()

rebuild = args.rebuild
IsDebug = args.debug
predict = args.predict

#控制预测哪个文件
lstP = ['./TEST/Test_reviews.csv','./TRAIN/Train_reviews.csv']

#复制数据入口： /data/reviews.csv
strCmd = 'cp %s ./data/reviews.csv' % lstP[predict]
ret = os.system(strCmd) 

'''
#2019/8/30 todo: 优化步骤，把任务写成任务包，提取每步的说明与命令自动执行
思路：把每个步骤统一成一个执行方法, 参数以字典方式传入
dicCmd = {
    'begin':'', #开始的提示
    'cmd':[],   #命令行，
    'end':'',   #结束的提示
    'predict':1,#只有预测模型才执行
    }
'''

#任务包清单
lstCommands = [
    {
    'begin':'STEP 1: 原始数据文件，生成序列标注数据文件...', #开始的提示
    'cmd':[
        'sudo python pre_Proecess.py -model 0 -rebuild %d ' % rebuild ,
        ],   #命令行，
    'end':'',   #结束的提示
    'predict':0

    },
    {
    'begin':'STEP 2: 调用标注模型进行标注预测...', #开始的提示
    'cmd':[
        'sudo python BERT_NER.py --do_predict=true',
        ],   #命令行，
    'end':'STEP 2: 标注模型预测完成。',   #结束的提示
    },
    {
    'begin':'STEP 3: 调用标注结果处理程序，把提取结果格式化...', #开始的提示
    'cmd':[
        'sudo python labelpick.py',
        ],   #命令行，
    'end':'',   #结束的提示
    },
    {
    'begin':'STEP 4: 把提取结果复制到属性模型和观点模型目录中...', #开始的提示
    'cmd':[
        'cp ./output/picklabel_test.txt ./Category/data/test.tsv',
        #'cp ./output/picklabel_test.txt ./Polarity/data/test.tsv',
        'sudo python pre_Proecess.py -model 0',
        ],   #命令行，
    'end':'',   #结束的提示
    },
    {
    'begin':'STEP 5: 调用属性模型和观点模型进行预测...', #开始的提示
    'cmd':[
        './m_predict.sh',
        ],   #命令行，
    'end':'STEP 5: 属性分类和观点分类预测完成。',   #结束的提示
    },
    {
    'begin':'STEP 6:调用处理工具把分类模型预测结果格式化...', #开始的提示
    'cmd':[
        'sudo python predictResult.py ./Category/',
        'sudo python predictResult.py ./Polarity/',
        ],   #命令行，
    'end':'',   #结束的提示
    },
    {
    'begin':'STEP 7: 正在合并最后结果...', #开始的提示
    'cmd':[
        'sudo python MergeResult.py',
        ],   #命令行，
    'end':'',   #结束的提示
    },
    {
    'begin':'STEP 8: 正在评估模型...', #开始的提示
    'cmd':[
        'sudo python modelscore.py',
        ],   #命令行，
    'end':'',   #结束的提示
    'predict':1
    },
]

##执行任务包
def RunCmds (lstCmds, IsDebug = 0, predict = 0):
    pass
    print('开始自动处理...')
    for x in lstCmds:
        if 'predict' in x.keys():
            if x['predict']!=predict:continue
                
        if x['begin']:
            print(x['begin'])

        for strCmd in x['cmd']:
            os.system(strCmd)
        
        if x['end']:
            print(x['end'])
        
        if IsDebug:
            bk = input("按回车键继续...")

#调用执行任务包
RunCmds(lstCommands, IsDebug = IsDebug, predict = predict)    

sys.exit(0)
#-----------以下为旧代码------------------------------

print('开始数据预测...')

print('STEP 1: 原始数据文件，生成序列标注数据文件...')
#strCmd = 'sudo python pre_Proecess.py -rebuild %d -predictfile %s' % (rebuild, pfile)
strCmd = 'sudo python pre_Proecess.py -rebuild %d ' % rebuild
ret = os.system(strCmd) 
if IsDebug:
    bk = input("按回车键继续：")

# STEP 2: 调用标注模型进行标注预测，得到结果
# ==>/output/(多个文件)

print('STEP 2: 调用标注模型进行标注预测...')

strCmd = 'sudo python BERT_NER.py --do_predict=true'
os.system(strCmd)
print('STEP 2: 标注模型预测完成。')
if IsDebug:
    bk = input("按回车键继续：")

# STEP 3: 调用标注结果处理程序，把提取结果格式化<---[结果1]
# ==>/output/picklabel_test.txt

print('STEP 3: 调用标注结果处理程序，把提取结果格式化...')
strCmd = 'sudo python labelpick.py'
os.system(strCmd)
if IsDebug:
    bk = input("按回车键继续：")

# STEP 4: 把提取结果复制到属性模型和观点模型目录中
# /output/picklabel_test.txt ==> /Category/data/test.tsv; /Polarity/data/test.tsv
print('STEP 4: 把提取结果复制到属性模型和观点模型目录中...')
os.system('cp ./output/picklabel_test.txt ./Category/data/test.tsv')
os.system('cp ./output/picklabel_test.txt ./Polarity/data/test.tsv')  
if IsDebug:
    bk = input("按回车键继续：")


#STEP 5: 调用属性模型和观点模型进行预测
print('STEP 5: 调用属性模型和观点模型进行预测...')

'''
#os.system('cd ./Polarity') #sudo python run_Polarity.py --do_predict=true
os.system('sudo python ./Polarity/run_Polarity.py --do_predict=true')
#os.system('cd ..')
bk = input("按回车键继续")

#os.system('cd ./Category') #sudo python run_Category.py --do_predict=true
os.system('sudo python ./Category/run_Category.py --do_predict=true')
#os.system('cd ..')
'''

strCmd = './m_predict.sh'
os.system(strCmd)
print('STEP 5: 属性分类和观点分类预测完成。')
if IsDebug:
    bk = input("按回车键继续：")


# STEP 6: 调用处理工具把分类模型预测结果格式化
# 得到两个结果文件<---[结果2]
# /Category/output/predict.csv
# /Polarity/output/predict.csv
print('STEP 6:调用处理工具把分类模型预测结果格式化...')
os.system('sudo python predictResult.py ./Category/')
os.system('sudo python predictResult.py ./Polarity/')
if IsDebug:
    bk = input("按回车键继续：")

# STEP 7: 把“结果1”和“结果2”合并成最后的输出结果
print('STEP 7: 正在合并最后结果...')
os.system('sudo python MergeResult.py')
if IsDebug:
    bk = input("按回车键继续：")

# STEP 8: 评估模型得分（仅针对训练数据进行预测时可用）
if predict:
    print('STEP 8: 正在评估模型...')
    os.system('sudo python modelscore.py')



if __name__ == '__main__':
    pass

