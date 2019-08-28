# Text-Opinion-Mining
电商评论观点挖掘



-----------------------------------------
## 序列标注思路 2019/8/26 xmxoxo

使用BIO数据标注模式，总共标注两个实体：AspectTerms,OpinionTerms
编码方式为："B-ASP", "I-ASP", "B-OPI", "I-OPI"
句子之间用空行分隔。

根据提供的训练数据如下(数据做了合并)：

```
,id,AspectTerms,A_start,A_end,OpinionTerms,O_start,O_end,Categories,Polarities,text
0,1,_, , ,很好,0,2,整体,正面,很好，超值，很好用
1,1,_, , ,超值,3,5,价格,正面,很好，超值，很好用
2,1,_, , ,很好用,6,9,整体,正面,很好，超值，很好用
3,2,_, , ,很好,0,2,整体,正面,很好，遮暇功能差一些，总体还不错
4,2,遮暇功能,3,7,差一些,7,10,功效,负面,很好，遮暇功能差一些，总体还不错
5,2,_, , ,还不错,13,16,整体,正面,很好，遮暇功能差一些，总体还不错
```

标注后的训练样本例子如下：

```
很 B-OPI
好 I-OPI
， O
超 B-OPI
值 I-OPI
， O
很 B-OPI
好 I-OPI
用 I-OPI

很 B-OPI
好 I-OPI
， O
遮 B-ASP
暇 I-ASP
功 I-ASP
能 I-ASP
差 B-OPI
一 I-OPI
些 I-OPI
， O
总 O
体 O
还 B-OPI
不 I-OPI
错 I-OPI
```

## 训练模型：

```
sudo python BERT_NER.py \
	--do_train=true \
	--do_eval=true \
	--do_predict=true \
	--data_dir=./data/ \
	--bert_config_file=../bert/chinese_L-12_H-768_A-12/bert_config.json \
	--init_checkpoint=../bert/chinese_L-12_H-768_A-12/bert_model.ckpt \
	--vocab_file=../bert/chinese_L-12_H-768_A-12/vocab.txt \
	--output_dir=./output/
```

## 预测数据(测试数据)：

```
sudo python BERT_NER.py \
	--do_train=False \
	--do_predict=true \
	--data_dir=./data/ \
	--bert_config_file=../bert/chinese_L-12_H-768_A-12/bert_config.json \
	--init_checkpoint=../bert/chinese_L-12_H-768_A-12/bert_model.ckpt \
	--vocab_file=../bert/chinese_L-12_H-768_A-12/vocab.txt \
	--output_dir=./output/
```

## 预测完后数据的处理
```
sudo python labelpick.py
```

会在`output`目录下生成合并结果文件(merge_test.txt) 和提取结果文件 (picklabel_test.txt)

在输出文件(picklabel_test.txt)中增加对应的记录ID号，样例如下：

```
id,index,txt,label
1,1,很好,OPI
1,4,超值,OPI
1,7,很好用,OPI
2,12,很好,OPI
2,15,遮暇功能,ASP
2,19,差一些,OPI
2,25,还不错,OPI
3,30,包装,ASP
3,32,太随便了,OPI
3,39,包装盒,ASP
3,43,没有,OPI
3,50,很不好,OPI

```


-----------------------------------------
## 情感分析

使用BERT情感分类模型，样本数据直接用训练数据中的 AspectTerms和 OpinionTerms 字段；

训练数据样例：

```
Polarities,AspectTerms,OpinionTerms
正面,,很好
正面,,超值
正面,,很好用
正面,,很好
负面,遮暇功能,差一些
正面,,还不错
负面,包装,太随便了
负面,包装盒,没有
负面,,很不好
负面,,非常的不好
负面,,垃圾
正面,,很是划算
```

训练集与验证集比例为8:2
样本数量为： 5306:1327
全数据：6633

预测数据暂时使用全部训练数据。

*** 训练模型并预测 ***

已在代码中直接指定了模型目录等参数，省去命令行带参数

```
cd Polarity
sudo python run_Polarity.py
```

训练结果：
```
eval_accuracy = 0.9389601
eval_f1 = 0.74708176
eval_loss = 0.19356915
eval_precision = 0.78688526
eval_recall = 0.7111111
global_step = 497
loss = 0.19369926

```

recall得分比较低，查看数据发现比较多重复的数据，由于文本内容比较少，有很多行完全相同。
把重复行删除，同时把两列合并为一列，重复训练。

训练结果：

```
eval_accuracy = 0.89719623
eval_f1 = 0.8186528
eval_loss = 0.3654422
eval_precision = 0.8061224
eval_recall = 0.83157897
global_step = 160
loss = 0.36228746
```

虽然acc了，但是由于 recall提升了，整体的F1值得到了提升。

## 属性分类模型 
由于数据相同，使用同一个训练数据；

分类labels:
['整体','使用体验','功效','价格','物流','气味','包装','真伪','服务','其他','成分','尺寸','新鲜度']

数据：
同样使用 pre_Proecess.py 来生成

```
Categories,text
使用体验,滋润度很好
使用体验,粉液一般般
价格,价位
气味,味道很好
物流,物流好快
功效,白的不自然
使用体验,起痘
```
数据目录: ./Category/data

开始训练模型：

```
cd Category
sudo python run_Category.py
```

训练结果：

```
eval_accuracy = 0.8640553
eval_f1 = 0.95714283
eval_loss = 0.55876833
eval_precision = 0.95988536
eval_recall = 0.954416
global_step = 162
loss = 0.5517428
```

得分还可以。


-----------------------------------------
##接下来的问题

* 解决标注后的关系

序列只标出实体，但没有提取关系
比如样本1标注结果：
```
1,a,ASP
1,b,OPI
1,c,OPI
```

但结果应该是

```
1 a,b
1 _,c
```

需要把a,b连接起来；


* 使用代码把预测结果文件处理成格式化结果

* 使用代码把整个工作串接起来，实现从样本到提交结果；

-----------------------------------------
## 预测结果格式化

分类模型预测结果格式化都是一样的，只要把预测结果中每行中的最大值索引取出，对应到标签即可；
标签字典统一存放为: label2id.pkl




