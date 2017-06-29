# -*- coding: utf-8 -*-
#-------------------------
#   版本：1.0
#   日期：2017年4月21日10:59:51
#   作者：kk
#-------------------------

from pymongo import *
class MongoDB(object):
    #mongoDB连接
    client = MongoClient("127.0.0.1", 27017)
    #选择库
    db = client["Sina_1"]
    def __init__(self):

        pass

    def getDB(self):
        return self.db

    def get_client(self):
        return self.client

    # 筛选 1--男  -1不筛选  其他是女
    def get_information_set_with_sex_flag(self,sexFlag):
        collection = self.db.Information
        list = collection.find()
        resultList = []
        #不需要筛选
        if sexFlag == -1:
            for person in list:
                resultList.append(person)
            return resultList

        #筛选 1--男 其他是女
        sex = u'男' if sexFlag == 1 else u'女'
        print sex
        for person in list:
            try:
                if person["Gender"] == sex:
                    resultList.append(person)
            except:
                print "dont have this tag"
        return resultList

    def get_tweets_by_id(self,person_id):
        collection = self.db.Tweets
        resultList = []
        for tweet in collection.find({"ID":person_id}):
            resultList.append(tweet)
        return resultList

    def get_information_by_id(self,person_id):
        collection = self.db.Information
        return collection.find_one({"_id":person_id})

    # 筛选 1--男 -1不筛选 其他是女
    def get_all_tweets_with_sex_flag(self,sexFlag):
        list = self.get_information_set_with_sex_flag(sexFlag)
        resultList = []
        for person in list:
            resultList.extend(self.get_tweets_by_id(person["_id"]))
        return resultList

    def get_test_data(self):
        list = self.db.Implicate.find()
        resultList = []
        for item in list:
            if  item["tweets_count"] > 10:
                resultList.append(item)

        return resultList

