import gensim
import pandas as pd
from nlp import NLP
from dataset_utils import *
import jieba

combined_dir = '../dataset/combined/'

assembled_combined_csv = pd.read_csv(combined_dir + 'assembled_combined.csv', quoting=3)
train_dataset, test_dataset = NLP.divide_train_test(assembled_combined_csv, '2016-02-01')

# date and label list




class NLPWithGensim:
    @classmethod
    def documents_to_tfidf_corpus(cls, documents):
        news_data = documents.values
        tokenized_news_list = []
        for daily_news in news_data:
            filtered_daily_news = []
            filtered_daily_news = [x for x in daily_news if str(type(x)).find('float') == -1]

            filtered_daily_news = ' '.join(filtered_daily_news)
            filtered_daily_news = list(jieba.cut(filtered_daily_news))
            tokenized_news_list.append(filtered_daily_news)
        dic = gensim.corpora.Dictionary(tokenized_news_list)
        corpus = [dic.doc2bow(text) for text in tokenized_news_list]
        tfidf = gensim.models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        # for doc in corpus_tfidf:
        #     print doc
        return corpus_tfidf, dic

    def __init__(self):
        pass


if __name__ == '__main__':
    documents = derive_components_from_dataset(train_dataset)[2]
    corpus_tfidf, dic = NLPWithGensim.documents_to_tfidf_corpus(documents)

    lda = gensim.models.LdaModel(corpus_tfidf, num_topics=10, id2word=dic)
    corpus_lda = lda[corpus_tfidf]
    print 'Print topics...'
    for i in range(10):
        print lda.print_topic(i)

