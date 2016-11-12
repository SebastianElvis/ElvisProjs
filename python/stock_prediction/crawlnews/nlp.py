# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import logging

class NLP:
    def __init__(self):
        self.djia_news_csv_dir = 'http://127.0.0.1:8000/static/dataset/Combined_News_DJIA.csv'
        self.dataset = pd.read_csv(self.djia_news_csv_dir)
        logging.debug('Read the dataset succeed!')
        self.train_dataset = self.dataset[self.dataset['Date'] < '2015-01-01']
        self.test_dataset = self.dataset[self.dataset['Date'] > '2014-12-31']
        self.basicmodel = None
        self.count_vectorizer = CountVectorizer()
 
    def getTrainHeadlines(self):
        trainheadlines = []
        for row in range(0,len(self.train_dataset.index)):
            trainheadlines.append(' '.join(str(x) for x in self.train_dataset.iloc[row,2:27]))
        return trainheadlines
        
    def getTrainSparseMatrix(self):
        count_vectorizer_train = self.count_vectorizer.fit_transform( self.getTrainHeadlines() ) #将trainheadlines转换为稀疏矩阵，表示每日的新闻里每个词出现的次数
        return count_vectorizer_train #basictrain是稀疏矩阵（sparse matrix） (x,y),x组数据，y组特征
        
    def startTrain(self):
        self.basicmodel = LogisticRegression() #逻辑回归分类器
        self.basicmodel = self.basicmodel.fit( self.getTrainSparseMatrix(), self.train_dataset["Label"]) #输入数据，分类目标，开始训练
        
    def regressionTest(self):
        testheadlines = []
        for row in range(0,len(self.test_dataset.index)):
            testheadlines.append(' '.join(str(x) for x in self.test_dataset.iloc[row,2:27]))
        basictest = self.count_vectorizer.transform(testheadlines)
        predictions = self.basicmodel.predict(basictest)
        return pd.crosstab(self.test_dataset["Label"], predictions, rownames=["Actual"], colnames=["Predicted"])
        
    
