# -*- coding: utf-8 -*-
#-------------------------
#   版本：1.0
#   日期：2017年4月24日15:27:05
#   作者：kk
#-------------------------

import jieba
import jieba.analyse
import codecs
import jieba.posseg as pseg
import re

"""
@描述           根据传入的content，分离其中的表情
@return         result_string-去除表情后的文本 emoticonList-表情List，无去重
"""
def split_emoticon(content):
    result_string = ""
    emoticonList = []
    for item in content.split(']'):
        try:
            if item.split('[', 1)[0]:
                result_string += item.split('[', 1)[0]
            if item.split('[', 1)[1]:
                # print len(item.split('[', 1)[1])
                result_string += item.split('[', 1)[1]
                if len(item.split('[', 1)[1])>9: #一个中文占3字节。表情只需要最多3个中文 可是发现了很多奇奇怪怪的表情。待定
                    result_string += item.split('[', 1)[1]
                else:
                    emoticonString = "[%s]"%(item.split('[', 1)[1])
                    emoticonList.append(emoticonString)
        except Exception as e:
            pass

    return result_string,emoticonList

"""
@描述           根据传入的content，分离表情，符号
@return         result_string-去除表情和符号后的文本 emoticonList-表情List，无去重  symbolList-去重
"""
def split_emoticon_and_symbol(content):
    sourceString,emoticonList = split_emoticon(content)
    result_string = replace_symbol(sourceString)
    symbolList = get_symbol(sourceString)
    return result_string,emoticonList,symbolList

def replace_symbol(str):
    return re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）><《》【】]+".decode("utf8"), "",str)

def get_symbol(str):
    set1, set2 = set(), set()
    for letter in str:
        set1.add(letter)
    for letter in replace_symbol(str):
        set2.add(letter)
    return list(set1-set2)

def cut_content(content,needFlag):
    # print content
    resultList = []
    if needFlag:
        for item in pseg.cut(content):
            resultList.append(item)
    else:
        for item in jieba.cut(content):
            resultList.append(item)
    return resultList



class WordsFilter(object):
    st = codecs.open('C:\Users\chenyx\Desktop\stopwords.txt')
    #添加停顿词 为了增加搜索效率，用dic
    stopwords = {}
    for line in st:
        line = line.strip()
        stopwords[line] = "1"
    print "stopwords ready"

    def __init__(self):

        pass

    def stopwords_filter(self,sentence):
        list = jieba.cut(sentence,cut_all=False)
        filter_sentence = ""
        for word in list:
            if word.encode('utf-8') in self.stopwords:
                pass
            else:
                filter_sentence += word
        return filter_sentence

    #tag -- 数量
    def get_keywords_with_tag(self,content,numberOfKeywords):
        jieba.analyse.set_stop_words("C:\Users\chenyx\Desktop\stopwords.txt")
        resultList = jieba.analyse.extract_tags(content,numberOfKeywords)
        return resultList

    def get_filter_result(self,tweetsList):
        print "filter!"
        count,totalCount = 0,0
        totalCount = len(tweetsList)
        totalContent = ""
        for tweet in tweetsList:
            count += 1
            print "current :   %d / %d"%(count,totalCount)
            print "filter: "+ tweet["Content"]
            totalContent += self.stopwords_filter(split_emoticon(tweet["Content"])[0])
        return totalContent



