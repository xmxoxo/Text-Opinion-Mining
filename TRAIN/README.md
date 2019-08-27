1. 本数据集为化妆品品类的评论数据。为保护品牌隐私，数据已做脱敏，相关品牌名等用**代替；

2. id字段作为唯一标识对应Train_reviews.csv中的评论原文和
Train_labels.csv中的四元组标签。一条评论可能对应多个四元组标签；

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

