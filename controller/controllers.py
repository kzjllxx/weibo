# -*- coding: utf-8 -*-
#-------------------------
#   版本：1.0
#   日期：2017年4月24日10:08:52
#   作者：kk
#-------------------------

from db.mongodb import MongoDB
from items.items import NominalItem
from items import items
from tools.wordstools import WordsFilter
from tools import wordstools
import codecs
import threading


class ImplicateController(object):
    _mongodb = MongoDB()

    def __init__(self):

        pass

    def cal_implicate_degree(self):
        peopleList = self._mongodb.get_information_set_with_sex_flag(-1)
        collection = self._mongodb.getDB()["Implicate"]

        for person in peopleList:
            print "current"+person["_id"]
            #初始化标签
            total,higherThan50,lessThan50 = 0,0,0
            #获取数据
            tweetsList = self._mongodb.get_tweets_by_id(person["_id"])
            #没有tweets做的处理
            if  len(tweetsList) == 0:
                continue

            for tweet in tweetsList:
                degree = items.cal_implicit_degree(tweet["Content"])
                if degree > 50:
                    higherThan50 += 1
                else:
                    lessThan50 += 1
                total += degree
            avg = total/float(len(tweetsList))
            sex = ""
            try:
                if person["Gender"]:
                    sex = person["Gender"]
                else:
                    sex = "空"
            except:
                print "dont have sex tag"

            data = {"_id":person["_id"],"implicit_degree":avg,"tweets_count":len(tweetsList),
                    "high_50":higherThan50,"less_50":lessThan50,"sex":sex}
            collection.insert(data)


class KeyWordsController(object):
    _mongodb = MongoDB()
    def __init__(self):
        pass

    def get_keywords_by_sex(self):
        filter = WordsFilter()
        #男性去掉停顿词后的集合
        male_total = filter.get_filter_result(self._mongodb.get_all_tweets_with_sex_flag(1))
        #女性去掉停顿词后的集合
        female_total = filter.get_filter_result(self._mongodb.get_all_tweets_with_sex_flag(2))

        #男性关键词
        maleKeyWordsList = filter.get_keywords_with_tag(male_total,200)
        # 女性关键词
        femaleKeyWordsList = filter.get_keywords_with_tag(female_total, 200)


        with codecs.open("C:\Users\chenyx\Desktop\NewDataSet\male_keyword_count.txt", "w", "utf-8") as f:
            for item in maleKeyWordsList:
                string = "%s\r\n" % (item)
                f.writelines(string)

        with codecs.open("C:\Users\chenyx\Desktop\NewDataSet\_female_keyword_count.txt", "w", "utf-8") as f:
            for item in femaleKeyWordsList:
                string = "%s\r\n" % (item)
                f.writelines(string)

class WordCountController(object):
    _mongodb = MongoDB()
    def __init__(self):
        pass

    def start_cal_by_words(self):
        """
        获取男性和女性的信息集合
        :return:
        """
        maleList = self._mongodb.get_information_set_with_sex_flag(1)
        femaleList = self._mongodb.get_information_set_with_sex_flag(0)

        male_emocionList,male_symbolList = self.main_function(maleList)
        female_emocionList, female_symbolList = self.main_function(femaleList)

        self.other_count(male_emocionList,male_symbolList,female_emocionList,female_symbolList)


    def main_function(self,list):
        index = 0
        length = len(list)
        e_List,s_List = [],[]
        for person in list:
            index += 1
            #数据初始化
            wordCount,letterCount = 0,0
            totalEmocionList,totalSymbolList = [],[]
            tweetList = self._mongodb.get_tweets_by_id(person["_id"])
            if len(tweetList) == 0:
                continue
            #收集数据
            for tweet in tweetList:
                formatContent,emocionList,symbolList = wordstools.split_emoticon_and_symbol(tweet["Content"])
                #词长
                wordCount += len(wordstools.cut_content(formatContent,False))
                #字长
                letterCount += len(formatContent)
                #表情
                totalEmocionList.extend(emocionList)
                #符号
                totalSymbolList.extend(symbolList)
            collection = self._mongodb.db.Implicate
            #更新数据 储存
            record = collection.find_one({"_id":person["_id"]})
            if record:
                record["word_avg"] = float(wordCount/float(len(tweetList)))
                record["letter_avg"] = float(letterCount/float(len(tweetList)))
                record["emocion_type"] = len(set(totalEmocionList))
                collection.save(record)

                #统计总数
                e_List.extend(totalEmocionList)
                s_List.extend(totalSymbolList)

                # 运行标识

                print "current: %s %d / %d ------- wordavg:%.2f  letteravg:%.2f" % (person["_id"],index, length,wordCount/float(len(tweetList)),letterCount/float(len(tweetList)))

        return e_List,s_List

    def other_count(self,m_e_list,m_s_list,f_e_list,f_s_list):
        male_emocionDic = dict()
        for item in set(m_e_list):
            male_emocionDic[item] = m_e_list.count(item)
        with codecs.open("C:\Users\chenyx\Desktop\NewDataSet\male_emocion_count.txt", "w", "utf-8") as f:
            for item in sorted(male_emocionDic.iteritems(), key=lambda a: a[1], reverse=True):
                string = "%s : %d \r\n" % (item[0], item[1])
                f.writelines(string)

        female_emocionDic = dict()
        for item in set(f_e_list):
            female_emocionDic[item] = f_e_list.count(item)
        with codecs.open("C:\Users\chenyx\Desktop\NewDataSet\_female_emocion_count.txt", "w", "utf-8") as f:
            for item in sorted(female_emocionDic.iteritems(), key=lambda a: a[1], reverse=True):
                string = "%s : %d \r\n" % (item[0], item[1])
                f.writelines(string)


from  tools.wordstools import WordsFilter
import os
from svmutil import *
class WordDifferenceController(object):
    _mongodb = MongoDB()
    def __init__(self):
        pass

    def test_method(self):
        all_users_list = self._mongodb.get_information_set_with_sex_flag(-1)
        male_flag, female_flag = 0, 0
        count = 0
        for user in all_users_list:


            try:
                user_tweets_list = self._mongodb.get_tweets_by_id(user["_id"])
                if len(user_tweets_list) < 10:
                    continue
                else:
                    count += 1
            except:
                print "wrong"

        print  count


    def count_difference(self):
        male_tweets_list = self._mongodb.get_all_tweets_with_sex_flag(1)
        female_tweets_list = self._mongodb.get_all_tweets_with_sex_flag(0)
        wf = WordsFilter()

        print  "analysis male"
        #分词 男性
        male_word_list = []
        index = 0
        for tweet in male_tweets_list:
            index += 1
            print "male: %d /  %d"%(index,len(male_tweets_list))
            male_word_list.extend(wordstools.cut_content(wf.stopwords_filter(wordstools.split_emoticon(tweet["Content"])[0]),False))



        print  "analysis female"
        index = 0
        #分词 女性
        female_word_list = []
        for tweet in female_tweets_list:
            index += 1
            print "female: %d /  %d" % (index, len(female_tweets_list))
            female_word_list.extend(wordstools.cut_content(wf.stopwords_filter(wordstools.split_emoticon(tweet["Content"])[0]),False))

        print "counting male"

        male_dic = dict()
        index = 0

        #统计word的次数
        for word in male_word_list:
            index += 1
            # print index
            if male_dic.has_key(word):
                male_dic[word] += 1
            else:
                male_dic[word] = 1

        print "counting female"
        index = 0
        female_dic = dict()
        for word in female_word_list:
            index += 1
            # print index
            # 统计word的次数
            if female_dic.has_key(word):
                female_dic[word] += 1
            else:
                female_dic[word] = 1

        for rate_int in range(11,51,1):
            #2.0做过了
            if rate_int == 20:
                continue

            male_only, female_only = dict(), dict()
            rate = float(rate_int) / 10
            print "current rate : %s" % rate
            file_path = "C:\Users\chenyx\Desktop\NewDataSet\%s" % (rate)
            os.makedirs(file_path)
            for word, times in male_dic.items():
                try:
                    if female_dic.has_key(word):
                        # 男性用词数大于女性的N倍
                        if (times / float(female_dic[word])) > rate:
                            male_only[word] = times
                        # 女性用词数大于男性的N倍
                        if (float(female_dic[word]) / times) > rate:
                            female_only[word] = female_dic[word]
                except Exception as e:
                    print e

            # 写数据
            # 男性
            url = file_path + "\male_all_word_count.txt"
            with codecs.open(url, "w", "utf-8") as f:
                for item in sorted(male_dic.iteritems(), key=lambda a: a[1], reverse=True):
                    string = "%s : %d \r\n" % (item[0], item[1])
                    f.writelines(string)
            url = file_path + "\male_only.txt"
            with codecs.open(url, "w", "utf-8") as f:
                for item in sorted(male_only.iteritems(), key=lambda a: a[1], reverse=True):
                    string = "%s : %d \r\n" % (item[0], item[1])
                    f.writelines(string)

            # 女性
            url = file_path + "\_female_all_word_count.txt"
            with codecs.open(url, "w", "utf-8") as f:
                for item in sorted(female_dic.iteritems(), key=lambda a: a[1], reverse=True):
                    string = "%s : %d \r\n" % (item[0], item[1])
                    f.writelines(string)
            url = file_path + "\_female_only.txt"
            with codecs.open(url, "w", "utf-8") as f:
                for item in sorted(female_only.iteritems(), key=lambda a: a[1], reverse=True):
                    string = "%s : %d \r\n" % (item[0], item[1])
                    f.writelines(string)



            print "start counting!"
            index = 0
            all_users_list = self._mongodb.get_information_set_with_sex_flag(-1)
            male_flag,female_flag = 0,0
            for user in all_users_list:

                index += 1
                print "%.2f---final: %d /  %d" % (rate,index, len(all_users_list))
                try:
                    user_tweets_list = self._mongodb.get_tweets_by_id(user["_id"])
                    if len(user_tweets_list) < 10:
                        continue
                    sex_flag = 0
                    if user["Gender"] == u'男':
                        sex_flag = 1
                        male_flag += 1
                    elif user["Gender"] == u'女':
                        sex_flag = -1
                        female_flag += 1
                    else:
                        continue


                    person_word_list = []
                    # 男性次跟女性词一共出现了多少次
                    male_bingo, female_bingo = 0, 0
                    # 男性次跟女性词一共有多少个（去重的）
                    male_word_set, female_word_set = 0, 0
                    for tweet in user_tweets_list:
                        person_word_list.extend((wordstools.cut_content(
                            wf.stopwords_filter(wordstools.split_emoticon(tweet["Content"])[0]), False)))
                    for word in set(person_word_list):
                        if male_only.has_key(word):
                            male_bingo = male_bingo + person_word_list.count(word)
                            male_word_set += 1
                        elif female_only.has_key(word):
                            female_bingo = female_bingo + person_word_list.count(word)
                            female_word_set += 1

                    string = "%d 1:%f 2:%f\r\n" % (sex_flag, (male_bingo + 1) / float(female_bingo + male_bingo + 1),
                                                   (male_word_set + 1) / float(1 + female_word_set + male_word_set))
                    if sex_flag == 1:

                        if male_flag > 50:
                            url = file_path + "\data_train.txt"
                        else:
                            url = file_path + "\data_test.txt"

                    else:
                        if female_flag > 50:
                            url = file_path + '\data_train.txt'
                        else:
                            url = file_path + '\data_test.txt'
                    with codecs.open(url, "a", "utf-8") as f:
                        f.writelines(string)

                except Exception as e:
                    print "final wrong"
                    print e
                finally:
                    pass
            #测试数据
            train_url = file_path + "\data_train.txt"
            test_url = file_path + "\data_test.txt"
            y, x = svm_read_problem(train_url)  # 读入训练数据
            yt, xt = svm_read_problem(test_url)  # 训练测试数据
            m = svm_train(y, x)  # 训练
            result = svm_predict(yt, xt, m)[1]  # 测试
            with codecs.open("C:\Users\chenyx\Desktop\NewDataSet\\result.txt", "a", "utf-8") as f:
                string = "%f ---- %f\r\n" %(rate,result[0])
                f.writelines(string)






    def start_content_analysis_with_threads(self,sex_tag,list):

        count = len(list)
        step = count/10 +1
        #线程池
        threads = []
        for i in range(10):
            start = i*step
            t = threading.Thread(target=self.content_dealer, args=(i,sex_tag,list[start:step+start],))
            t.setDaemon(True)
            threads.append(t)
        #开启线程
        for t in threads:
            t.start()
        #阻塞主线程
        for t in threads:
            t.join()

    def content_dealer(self, sequence, sex_tag, list):
        pass



class TestDataController(object):
    _mongodb = MongoDB()
    def __init__(self):
        pass

    def prepare_data(self):
        list = self._mongodb.get_test_data()
        index,total = 0,len(list)
        for item in list:
            index += 1
            print "current:  %d / %d"%(index,total)
            flag = 0
            if item["sex"] == u'男':
                flag = 1
            elif item["sex"] == u'女' :
                flag = -1
            else:
                continue

            implicit_degree = item["implicit_degree"]  #语言隐晦程度
            word_avg = item["word_avg"]  #平均词数
            letter_avg = item["letter_avg"]  #平均字数
            high_50 = item["high_50"]/float(item["tweets_count"])  #隐晦程度大于50的百分比
            less_50 = item["less_50"]/float(item["tweets_count"])  #隐晦程度小于50的百分比
            emocion_type = item["emocion_type"]  #使用的表情种类
            male_bingo = item["male_bingo"] #user的tweets集中一共用了多少次男性词汇
            female_bingo = item["female_bingo"]
            male_word_set = item["male_word_set"] #user的tweets集中一共用了多少 ge 男性词汇 去重的
            female_word_set = item["female_word_set"]

            person  = self._mongodb.get_information_by_id(item["_id"])
            tweets_own = item["tweets_count"] / float(person["Num_Tweets"])  #原创程度

            #语言隐晦程度 平均字数 平均次数 表情类型 原创程度
            #version-1  45%
            # string = "%d 1:%f 2:%f 3:%f 4:%f 5:%f 6:%d 7:%f\r\n" % (flag,implicit_degree,word_avg,letter_avg,high_50,less_50,emocion_type,tweets_own)

            #隐晦程度 平次词长 平均字数 表情类型
            ##version-2  55%
            # string = "%d 1:%f 2:%f 3:%f 4:%d \r\n" % (flag,implicit_degree, word_avg, letter_avg,emocion_type)

            #version-3  52% 平均词长 平均字数 隐晦程度
            # string = "%d 1:%f 2:%f 3:%f\r\n" % (flag, implicit_degree, word_avg, letter_avg)

            # version-4 50% 隐晦程度
            # string = "%d 1:%f\r\n" % (flag, implicit_degree)
            # if flag == 1:
            #     with codecs.open("C:\Users\chenyx\Desktop\NewDataSet\male_train_data3.txt", "a", "utf-8") as f:
            #         f.writelines(string)
            # else:
            #     with codecs.open("C:\Users\chenyx\Desktop\NewDataSet\_female_train_data3.txt", "a", "utf-8") as f:
            #         f.writelines(string)

            # version-5 52【300train 100test】/100[160tran 40test] 专属词汇
            # string = "%d 1:%d 2:%d 3:%d 4:%d\r\n" % (flag, male_bingo,male_word_set,female_bingo,female_word_set)
            # if flag == 1:
            #     with codecs.open("C:\Users\chenyx\Desktop\NewDataSet\\test-5\male_train_data5.txt", "a", "utf-8") as f:
            #         f.writelines(string)
            # else:
            #     with codecs.open("C:\Users\chenyx\Desktop\NewDataSet\\test-5\_female_train_data5.txt", "a", "utf-8") as f:
            #         f.writelines(string)

            #version-6 87% 专署词汇-归一化版本
            string = "%d 1:%f 2:%f\r\n" % (flag, (male_bingo+1)/float(female_bingo+male_bingo+1), (male_word_set+1)/float(1+female_word_set+male_word_set))
            if flag == 1:
                with codecs.open("C:\Users\chenyx\Desktop\NewDataSet\\test-6\male_train_data5.txt", "a", "utf-8") as f:
                    f.writelines(string)
            else:
                with codecs.open("C:\Users\chenyx\Desktop\NewDataSet\\test-6\_female_train_data5.txt", "a","utf-8") as f:
                    f.writelines(string)


