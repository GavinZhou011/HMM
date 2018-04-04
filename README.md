#隐马尔科夫模型进行中文分词
author : darrenan
created at : 2014-03-17

author : GavinZhou011
update at : 2017-04

监督学习方法，利用极大似然估计法来估计隐马尔科夫模型的参数。利用维特比算法预测。

#模型训练
python HMM_train.py [train_file]
./dataset/pku_training.utf8 #bakeoff语料，Microsoft Research
./dataset/msr_training.utf8 #bakeoff语料，Peking University

#关于语料
http://sighan.cs.uchicago.edu/bakeoff2005/
http://www.52nlp.cn/%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D%E5%85%A5%E9%97%A8%E4%B9%8B%E8%B5%84%E6%BA%90

#生成三个文件
* prob_start.py 为模型的初始状态概率
* prob_trans.py 为模型状态转移概率
* prob_emit.py 为发射（观测）概率

#对未分词数据文件test_file分词，生成test_seg_file文件
python HMM.py [test_file] [test_seg_file]

#分词测评结果
perl ./dataset/score [*_training_words.utf8] [*_test_gold.utf8] [test_seg_file]

#reference
* 维特比算法：http://zh.wikipedia.org/wiki/%E7%BB%B4%E7%89%B9%E6%AF%94%E7%AE%97%E6%B3%95
* https://github.com/fxsjy/
