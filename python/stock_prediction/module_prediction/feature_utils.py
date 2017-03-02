import re
from snownlp import SnowNLP
import pymongo

class ContentFeature:
    """

    """
    def __init__(self, content):
        self.content_feature_dict = dict()
        self.content_feature_dict['is_mention'] = self.is_mention(content)
        self.content_feature_dict['hashtag_list'] = self.find_hashtag_list(content)
        self.content_feature_dict['sentiment'] = self.get_sentiment(content)

    @classmethod
    def is_mention(cls, content):
        """
        Test if the content mentions others
        :param content: str which is the weibo content
        :return: 1 if mentioning others else 0
        """
        if '@' in content:
            return 1
        else:
            0

    @classmethod
    def find_hashtag_list(cls, content):
        """
        Find all hashtags in the content
        :param content: str which is the weibo content
        :return: list of the hashtags in the content
        """
        hashtag_list = list()
        pattern_hashtag = re.compile('#(.+?)#')
        match = pattern_hashtag.findall(content)
        if match:
            hashtag_list = match
        return hashtag_list

    @classmethod
    def get_sentiment(cls, content):
        """
        Compute the sentiment of the topic
        :param content: the weibo content
        :return: the value of the sentiment
        """
        s = SnowNLP(content)
        return s.sentiments
    # todo feature engineering!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def extract_features(record_dict):
    """
    (Experimental!)
    Extract the features from the weibo record object.
    Features: adv, neg, sent, punc, hashtag, is_mention, is_forwarded, forward_num, like_num, comment_num
    :param record_dict: record.__dict__(Record object's dict notation) which describes a weibo record
    :return: A dictionary which indicates the features of a single weibo record
    """
    feature_dict = dict()
    feature_dict['is_forwarded'] = 1 if record_dict['is_forwarded'] is True else False
    feature_dict['forward_num'] = record_dict['forward']
    feature_dict['like_num'] = record_dict['like']
    feature_dict['comment_num'] = record_dict['comment']

    # processing the content
    content = record_dict['content']
    feature_dict['content'] = content
    # merge the dict with the detailed features
    cf = ContentFeature(content)
    feature_dict.update(cf.content_feature_dict)

    return feature_dict

if __name__ == '__main__':
    r = pymongo.MongoClient().get_database('weibo').get_collection('record').find({'is_forwarded': False})
    for s in r:
        print extract_features(s)