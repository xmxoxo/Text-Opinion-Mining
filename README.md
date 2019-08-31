# 电商评论观点挖掘 参赛日志
Text-Opinion-Mining


-----------------------------------------
比赛说明：

1. 本数据集为化妆品品类的评论数据。为保护品牌隐私，数据已做脱敏，相关品牌名等用**代替；
2. id字段作为唯一标识对应Train_reviews.csv中的评论原文和Train_labels.csv中的四元组标签。
一条评论可能对应多个四元组标签；

3. Train_labels.csv中的A_start和A_end表示AspectTerm在评论原文中的起始位置；
O_start和O_end表示OpinionTerm在评论原文中的起始位置。
若AspectTerm为"_",则A_start和A_end为空，OpinionTerm同理；
（注：预测结果不需要位置信息，仅考察四元组的预测情况）

4. AspectTerm和OpinionTerm字段抽取自评论原文，与原文表述保持一致。
若AspectTerm或OpinionTerm为空，则用“_”表示；
5. Category字段的结果属于以下集合（具体以训练集为准）：
{ 包装，成分，尺寸，服务，功效，价格，气味，使用体验，物流，新鲜度，真伪，整体，其他 }
6. Polarity字段的结果属于以下集合（具体以训练集为准）：
{ 正面、中性、负面 }

-----------------------------------------
2、字段说明：
（1）评论ID（ID)：ID是每一条用户评论的唯一标识。
（2）用户评论（Reviews）：用户对商品的评论原文。
（3）属性特征词（AspectTerms）：评论原文中的商品属性特征词。
例如“价格很便宜”中的“价格”。该字段结果须与评论原文中的表述保持一致。
（4）观点词（OpinionTerms）：评论原文中，用户对商品某一属性所持有的观点。
例如“价格很便宜”中的“很便宜”。该字段结果须与评论原文中的表述保持一致。
（5）观点极性（Polarity）：用户对某一属性特征的观点所蕴含的情感极性，即负面、中性或正面三类。
（6）属性种类（Category）：相似或同类的属性特征词构成的属性种类。
例如“快递”和“物流”两个属性特征词都可归入“物流”这一属性种类。
我们规定了属性种类集合（详见训练数据README.md）,该字段结果应属于该集合。

-----------------------------------------

四、评分标准
1、相同ID内逐一匹配各四元组，若AspectTerm，OpinionTerm，Category，Polarity四个字段均正确，则该四元组正确；
2、预测的四元组总个数记为P；真实标注的四元组总个数记为G；正确的四元组个数记为S：
（1）精确率： Precision=S/P
（2）召回率： Recall=S/G
（3）F值:F1-score=(2*Precision*Recall)/(Precision+Recall)

-----------------------------------------
## 目录结构说明
最后更新： 2019/8/28 14:26
```
Text-Opinion-Mining
├─Category	属性分类模型	
│  ├─data		分类数据目录
│  └─output		分类输出目录
├─data		标注模型数据目录
├─log		日志目录（未使用）
├─output	标注模型输出目录
│  ├─testdat	标注模型，测试文件输出目录
│  └─traindat	标注模型，训练数据输出目录
├─Polarity	观点分类模型
│  ├─data		数据目录
│  ├─data_0
│  ├─data_1
│  ├─output		输出目录与数据目录对应
│  ├─output_0
│  ├─output_1
│  └─output_2
├─TEST		原始测试数据
└─TRAIN		原始训练数据
```
最新结构见tree.txt
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

### 训练模型：

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

### 预测数据(测试数据)：

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
## 观点分类模型

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
sudo python run_Polarity.py --do_train=true --do_eval=true
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
\Polarity\output_2\eval_results.txt

eval_accuracy = 0.89719623
eval_f1 = 0.8186528
eval_loss = 0.3654422
eval_precision = 0.8061224
eval_recall = 0.83157897
global_step = 160
loss = 0.36228746
```

虽然acc了，但是由于 recall提升了，整体的F1值得到了提升。

-----------------------------------------
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
##接下来的问题 [2019/8/28 13:47]

* 解决标注后的关系

* 使用代码把预测结果文件处理成格式化结果

* 使用代码把整个工作串接起来，实现从样本到提交结果；

-----------------------------------------
## 预测结果格式化 [2019/8/28 14:07]

分类模型预测结果格式化都是一样的，只要把预测结果中每行中的最大值索引取出，对应到标签即可；
标签字典统一存放为: label2id.pkl

需要的参数：
	测试文件 ./data/test.tsv; 
	标签字典, ./output/label2id.pkl
	预测结果, ./output/test_results.tsv (注意：编码是936)
输出结果文件：./output/predict.csv

程序命令行规划： predictResult.py 目录名
在指定的目录下自动寻找相应的文件。
结果文件输出列为： label,内容为标签中文值

处理命令行：

```
predictResult.py ./Category/
predictResult.py ./Polarity/
```
处理完后有两个文件生成：

```
/Category/output/predict.csv
/Polarity/output/predict.csv
```

分别是属性分类和观点分类结果

-----------------------------------------
## 解决标注后的关系

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

这个关系需要按照语义来划分，感觉比较复杂。
看了下数据,基本上属性和观点都在一个短句里面，那就先简单的按标点符号来吧。
写下思路：

原句子, 直接从原始文件中读出来(Train_reviews.csv)：
```
6,使用一段时间才来评价，淡淡的香味，喜欢！
```

序列化输出的结果是：
```
id,index,txt,label
6,128,淡淡的,OPI
6,131,香味,ASP
6,134,喜欢,OPI
```

先把原句按标点符号分开下，标点符号包括：`['，' , '；' , '。' , '！']`
原句分成三个小句：

```
使用一段时间才来评价，
淡淡的香味，
喜欢！
```

然后根据序列化输出的位置，看下各个结果在哪个小句中：

```
输出的三句：
使用一段时间才来评价，   《==没有
淡淡的香味，             《==淡淡的,OPI    香味,ASP
喜欢！                   《== 喜欢,OPI
```

于是组合出来两个结果：

```
id, ASP, OPI 
6,香味,淡淡的
6,_,喜欢
```

-----------------------------------------
## 整合全流程(预测)

使用代码把整个工作串接起来，实现从样本到最后的提交结果。

流程步骤整理:

```
#STEP 1: 原始数据文件，生成序列标注数据文件
#/TEST/Test_reviews.csv  ==> /data/test.txt

#STEP 2: 调用标注模型进行标注预测，得到结果
#==>/output/(多个文件)

#STEP 3: 调用标注结果处理程序，把提取结果格式化<---[结果1]
#==>/output/picklabel_test.txt

#STEP 4: 把提取结果复制到属性模型和观点模型目录中
#/output/picklabel_test.txt ==> /Category/data/test.tsv; /Polarity/data/test.tsv

#STEP 5: 调用属性模型和观点模型进行预测

#STEP 6: 调用处理工具把分类模型预测结果格式化
#得到两个结果文件<---[结果2]
#==> /Category/output/predict.csv
#==> /Polarity/output/predict.csv

#STEP 7: 把“结果1”和“结果2”合并成最后的输出结果
#==>/output/Result.csv
```

把整个流程整理到一个文件：run_Predict.py

```
使用命令行：
python run_Predict.py rebuild IsDebug
参数：  
    rebuild 强制生成数据，默认0
    IsDebug 调试模式，每步都等确认；默认0

快速预测：python run_Predict.py
重生成数据并预测：python run_Predict.py 1
调试模式预测：python run_Predict.py 1 1
```
-----------------------------------------
## 模型评估

模型评价工具 modelscore.py

```
四、评分标准
1、相同ID内逐一匹配各四元组，若AspectTerm，OpinionTerm，Category，Polarity四个字段均正确，则该四元组正确；
2、预测的四元组总个数记为P；真实标注的四元组总个数记为G；正确的四元组个数记为S：
（1）精确率： Precision=S/P
（2）召回率： Recall=S/G
（3）F值:F1-score=(2*Precision*Recall)/(Precision+Recall)
```
根据上面的说明，整理出一个评估工具 

命令行格式: 
python modelscore.py -h
python modelscore.py 原始数据文件 预测结果文件

参数说明：
    原始数据文件: 原始数据文件或者训练数据文件，默认为 ./TRAIN/Train_labels.csv
    预测结果文件：模型预测输出的结果文件，默认值为 ./output/Result.csv

快速进行评价： python modelscore.py
指定文件评价： python modelscore.py ./data/labels.csv ./output1/Result.csv
-----------------------------------------
## 模型优化 
2019/8/30

昨天提交的结果在官方的得分是 0.6740

使用模型评估工具，在训练集上的评估得分情况：

```
===========抽取模型评估得分===========
P:7686 G:6633 S:4574
精确率: 0.595
召回率: 0.690
F1得分: 0.639
===========完整模型评估得分===========
P:7686 G:6633 S:4250
精确率: 0.553
召回率: 0.641
F1得分: 0.594
```

抽取结果的得分中，精确率比较低。需要做一些优化。

**分句方式** 
查看了一下分句的处理方式，是用标点符号来分隔的，查看了一下训练数据，有很多是用空格来分隔的。
于是在分句处理上加上了空格处理。
处理前提取结果： 7663条
处理后提取结果： 7683条

多了20条记录，继续完成分类与情感的预测，评估最后的结果：

```
===========抽取模型评估得分===========
P:7708 G:6633 S:4596
精确率: 0.596
召回率: 0.693
F1得分: 0.641
===========完整模型评估得分===========
P:7708 G:6633 S:4270
精确率: 0.554
召回率: 0.644
F1得分: 0.595
```
还是有了一点点的提高,这个修改保留。


**精确度优化**

从模型评估数据中可以看到精确率比较差，主要是固定抽取出来的结果P太大，
也就是抽取了太多的结果出来，这个比例是： `6633/7708 = 86.05%`

查看数据情况,有些标注的结果没有正确组合到一起，导致了抽取结果太多：
原句：
```
3215,挺超值的，补水效果不错，还会来买。
```
标注完的结果为：
```
id,index,txt,label,index_new,subPos
3215,76164,挺超值的,OPI,33,
3215,76169,补水效果,ASP,38,
3215,76173,不错,OPI,42,
```
最后组合后的结果为：
```
3215,_,不错,整体,正面
3215,补水效果,_,功效,正面
3215,_,挺超值的,价格,正面
```
而正确的结果应该是：
```
3215,补水效果,5,9,不错,9,11,功效,正面
3215,_, , ,挺超值的,0,4,价格,正面
```
可以看出，"补水效果" 和 "不错" 应该组合在一起的，没有正确组合。


标注提取问题，有些标注结果并不是连续的，跨了句子
原数据:
```
145,已经用的第三瓶了，以前一直用的绿色，这次换了紫色，不过还是一如既往的好用啊。美白还可以遮暇，大大的赞
146,之前用的瓶装紫色的，不太适合我，这个很好用，喜欢，好评
```

标注结果第3706行开始的数据：
```
美	B-OPI
白	I-OPI
还	O
可	O
以	O
遮	B-OPI
暇	I-OPI
，	O
大	O
大	I-OPI
的	I-OPI
赞	B-OPI
[SEP]	[SEP]
[CLS]	[CLS]
之	O
前	O
用	O
的	O
瓶	O
装	O
紫	O
色	O
的	O
，	O
不	O
太	I-OPI
适	O
合	I-OPI
我	O
，	O
这	O
个	O
```

重新调整标注结果的提取过程，解决以下三个问题：
句子起始索引号错误；
标注结果跨句子；
标注结果不连续；

解决后提取的结果为：6938行；

继续进行属性分类和观点分类的预测，形成最终结果，模型评估结果为：

```
===========抽取模型评估得分===========
P:6938 G:6633 S:5897
精确率: 0.850
召回率: 0.889
F1得分: 0.869
===========完整模型评估得分===========
P:6938 G:6633 S:5489
精确率: 0.791
召回率: 0.828
F1得分: 0.809
```
-----------------------------------------
## 模型评估bug

在评估模型时，思路是“把预测结果的每一个数据与正确结果对比，如果存在则正确数加1”
这样可能会有重复出现的同一个预测结果重复计算了次数，
改正的方法是反过来:“把正确结果中的每个数据与预测结果对比，如果存在则正确数加1”。
但这样就不知道重复了多少次，于是还是用原来的思路，
但是增加了setRet集合来保存记录的结果，最后计算setRet集合的大小就是唯一正确数，
而累加数就是正确的个数,包含了重复的数据。

```
===========抽取模型评估得分===========
唯一正确：5889, 正确个数:5897
P:6938 G:6633 S:5889
精确率: 0.849
召回率: 0.888
F1得分: 0.868
===========完整模型评估得分===========
唯一正确：5482, 正确个数:5489
P:6938 G:6633 S:5482
精确率: 0.790
召回率: 0.826
F1得分: 0.808
```
-----------------------------------------
生成测试数据的标注文件: python pre_Process.py -predictfile ./TEST/Test_reviews.csv

-----------------------------------------
## CRF-NER模型：

提取：
```
   id   ASP    OPI
0   1     _     很好
1   1     _     超值
2   1     _    很好用
3   2     _     很好
4   2  遮暇功能    差一些
5   2     _    还不错
6   3    包装   太随便了
7   3   包装盒     没有
8   3     _    很不好
9   4     _  非常的不好
提取记录数: 6953
提取结果保存完成: ./output/picklabel_test.txt
```


预测完后进行评估：
```
===========抽取模型评估得分===========
唯一正确：5802, 正确个数:5802
P:6953 G:6633 S:5802
精确率: 0.834
召回率: 0.875
F1得分: 0.854
===========完整模型评估得分===========
唯一正确：5400, 正确个数:5400
P:6953 G:6633 S:5400
精确率: 0.777
召回率: 0.814
F1得分: 0.795
```
得分并没有提高 ，还是用原来的模型吧。
-----------------------------------------
## 一键执行  [2019/8/30 18:45]

目前仅支持linux下运行。

一键完成**测试数据**的全流程**预测**处理，生成最后的提交文件：
```
sudo python run_Predict.py -predict 0 -rebuild 1
```

一键完成**训练数据**的全流程**预测**处理，生成最后的提交文件：
```
sudo python run_Predict.py -predict 1 -rebuild 1
```
-----------------------------------------
## 分类模型优化

对观点分类模型进行优化，修改训练数据，使用提取结果词所在的分句作为训练样本。

跑完的结果：
```
eval_accuracy = 0.9603624
eval_f1 = 0.88429755
eval_loss = 0.14791998
eval_precision = 0.89166665
eval_recall = 0.8770492
global_step = 331
loss = 0.1482842
```


***数据检查*** 

问题：

data_merge.csv 中，203行，“好”字的索引应该是7,而不是8
```
201,94,_,好用,,0.0,好用，服务态度好
202,94,服务态度,_,3.0,,好用，服务态度好
203,94,_,好,,8.0,好用，服务态度好
```
查源头：
picklabel_test.txt 文件中提取的O_start就是8而不是7
```
94,_,好用,,0
94,服务态度,_,3,
94,_,好,,8
```
再往前查：
seg_test.txt 中，2279内容行 
  索引应该是7而不是8；
  所在分句应该是3，而不是0；
```
94,2272,好用,OPI,2271,0,1
94,2275,服务态度,ASP,2271,3,2
94,2279,好,OPI,2271,8,0
```
原因是：在循环提以标注结果时，标注内容在哪一句原来是自动累加的，
遇到某一句没有任何标注（例如219句只有一个字），则会出错。
改成： 使用getid(index)方法，按索引位置来计算句子号就不会出错了。

修改后的结果：`seg_test.txt`
```
94,2272,好用,OPI,2271,0,1
94,2275,服务态度,ASP,2271,3,2
94,2279,好,OPI,2271,7,2
```
再往后：`picklabel_test.txt`
```
94,_,好用,,0
94,服务态度,好,3,7
```
提取数据： 6940行

合并后的数据： data_merge.csv
```
202,94,服务态度,好,3.0,7.0,好用，服务态度好
```
数据正确了



***调整后模型评估***

```
===========抽取模型评估得分===========
唯一正确：5910, 正确个数:5918
P:6921 G:6633 S:5910
精确率: 0.854
召回率: 0.891
F1得分: 0.872
===========完整模型评估得分===========
唯一正确：5559, 正确个数:5566
P:6921 G:6633 S:5559
精确率: 0.803
召回率: 0.838
F1得分: 0.820
```
-----------------------------------------
## 使用最新模型生成提交数据

```
sudo python run_Predict.py -predict 0 -rebuild 1 -debug 1
```

```
   id AspectTerms OpinionTerms Categories Polarities
0   1           _          是正品         真伪         正面
1   1           _           白嫩       使用体验         正面
2   1           _           不错         整体         正面
3   2           _        不是我喜欢         整体         负面
4   2          颜色           明显         功效         正面
5   3           _         挺细腻的       使用体验         正面
6   4           _          还行吧         整体         正面
7   5           _           不错         整体         正面
8   6           _          很细腻       使用体验         正面
9   6           _         贴合肤色       使用体验         正面
------------------------------
总条数：4854, 最大ID：2237, 缺失ID数：0
最终结果已经保存:./output/Result.csv
```
