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
	--data_dir=./TRAIN/ \
	--bert_config_file=../bert/chinese_L-12_H-768_A-12/bert_config.json \
	--init_checkpoint=../bert/chinese_L-12_H-768_A-12/bert_model.ckpt \
	--vocab_file=../bert/chinese_L-12_H-768_A-12/vocab.txt \
	--output_dir=./output/
```

## 预测数据(测试数据)：

```
sudo python BERT_NER.py \
	--do_predict=true \
	--data_dir=./TRAIN/ \
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






