# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import logging
import re
import jieba
import os

logger = logging.getLogger("django")

def is_contain_zh(str):
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zh_pattern.search(str)
    return True if match else False


class NLP:
    # vectorizer
    vectorizer = TfidfVectorizer()

    @classmethod
    def _get_daily_data_collection(cls, dataset):
        raw_daily_data = []
        for row in range(0, len(dataset.index)):
            one_day_data = ' '.join([str(x) for x in dataset.iloc[row, 2:-1]])
            if is_contain_zh(one_day_data):
                one_day_data = ' '.join(jieba.cut(one_day_data))
            raw_daily_data.append(one_day_data)
        return raw_daily_data

    @classmethod
    def _get_sparse_matrix(cls, dataset):
        # 将raw daily data转换为稀疏矩阵，表示每日的新闻里每个词出现的次数
        sparse_matrix = NLP.vectorizer.fit_transform(NLP._get_daily_data_collection(dataset))
        # sparse_matrix是稀疏矩阵（sparse matrix） (x,y),x组数据，y组特征
        return sparse_matrix

    @classmethod
    def divide_train_test(cls, dataset, divide_date):
        train_dataset = dataset[dataset['Date'] < divide_date]
        test_dataset = dataset[dataset['Date'] >= divide_date]
        return train_dataset, test_dataset

    def __init__(self):
        logger.debug('Init NLP Object')

        #print os.listdir('../dataset/combined/'.decode('utf-8'))

        # initialize the dataset
        self.djia_news_csv_dir = '..\dataset\Combined_News_DJIA.csv'
        self.dataset = pd.read_csv(self.djia_news_csv_dir)
        logger.debug('Read the dataset succeed!')
        self.train_dataset, self.test_dataset = NLP.divide_train_test(self.dataset, '2015-04-01')

        # different models for different dataset
        self.financial_model = None
        self.tech_model = None
        self.company_model = []
        
        # train the model
        logger.debug('Start to train NLP Model')
        self.start_train('financial')
        logger.info('Train NLP Model success!')
        
        # test the model
        logger.debug("Start regression test")
        rt = self.regression_test()
        logger.info(rt)
        logger.debug('Regression test successful')

    def start_train(self, model_type='financial'):
        if model_type is 'financial':
            self.financial_model = LogisticRegression()  # 逻辑回归分类器
            self.financial_model = self.financial_model.fit(NLP._get_sparse_matrix(self.train_dataset),  # 每日数据
                                                            self.train_dataset["Label"])  # 每日结果
        elif model_type is 'tech':
            self.tech_model = LogisticRegression()  # 逻辑回归分类器
            self.tech_model = self.tech_model.fit(NLP._get_sparse_matrix(self.train_dataset),  # 每日数据
                                                  self.train_dataset["Label"])  # 每日结果
        else:  # TODO
            pass

    def regression_test(self, model_type='financial'):
        test_sparse_matrix = NLP.vectorizer.transform(NLP._get_daily_data_collection(self.test_dataset))
        # predictions is an index array which indicates the predictioin result of the test dataset
        if model_type is 'financial':
            predictions = self.financial_model.predict(test_sparse_matrix)
        elif model_type is 'tech':
            predictions = self.tech_model.predict(test_sparse_matrix)
        else:  # TODO
            predictions = None
            pass

        # type(result) -> pandas.core.frame.DataFrame
        result = pd.crosstab(self.test_dataset["Label"], predictions, rownames=["Actual"], colnames=["Predicted"])
        return result


logger.debug('Start to initialize the NLP Object')
nlp_model = NLP()
logger.debug('Initialize the NLP Object successfully')
