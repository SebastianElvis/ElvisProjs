# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

data = pd.read_csv('templates/vendor/dataset/Combined_News_DJIA.csv')

train = data[data['Date'] < '2015-01-01']
test = data[data['Date'] > '2014-12-31']

example = train.iloc[3,10]
print(example)

example2 = example.lower()
print(example2)

example3 = CountVectorizer().build_tokenizer()(example2)
print(example3)

pd.DataFrame([[x,example3.count(x)] for x in set(example3)], columns = ['Word', 'Count'])

trainheadlines = []
for row in range(0,len(train.index)):
    trainheadlines.append(' '.join(str(x) for x in train.iloc[row,2:27]))
    
basicvectorizer = CountVectorizer()
basictrain = basicvectorizer.fit_transform(trainheadlines) #将trainheadlines转换为稀疏矩阵，表示每日的新闻里每个词出现的次数
print(basictrain.shape) #basictrain是稀疏矩阵（sparse matrix） (x,y),x组数据，y组特征

basicmodel = LogisticRegression() #逻辑回归分类器
basicmodel = basicmodel.fit(basictrain, train["Label"]) #输入数据，分类目标，开始训练

#回归测试
testheadlines = []
for row in range(0,len(test.index)):
    testheadlines.append(' '.join(str(x) for x in test.iloc[row,2:27]))
basictest = basicvectorizer.transform(testheadlines)
predictions = basicmodel.predict(basictest)

pd.crosstab(test["Label"], predictions, rownames=["Actual"], colnames=["Predicted"])

basicwords = basicvectorizer.get_feature_names()
basiccoeffs = basicmodel.coef_.tolist()[0]
coeffdf = pd.DataFrame({'Word' : basicwords, 
                        'Coefficient' : basiccoeffs})
coeffdf = coeffdf.sort_values(['Coefficient', 'Word'], ascending=[0, 1])
coeffdf.head(10)