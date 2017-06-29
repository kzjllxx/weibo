# -*- coding: utf-8 -*-
#-------------------------
#   版本：1.0
#   日期：2017年4月21日16:03:03
#   作者：kk
#-------------------------


# 进行隐晦性计算
# from controller.controllers import ImplicateController
# ic = ImplicateController()
# ic.cal_implicate_degree()

# from tools.wordstools import WordsFilter
# fi = WordsFilter()


# from controller.controllers import KeyWordsController
# keyword = KeyWordsController()
# keyword.get_keywords_by_sex()

# from controller.controllers import WordCountController
# wordC = WordCountController()
# wordC.start_cal_by_words()

from controller.controllers import WordDifferenceController

wc = WordDifferenceController()
wc.count_difference()
# wc.test_method()

# from controller.controllers import TestDataController
# testC = TestDataController()
# testC.prepare_data()


#####  test ######
# import codecs
# string = "%d 1:%f 2:%f\r\n" % (1 ,0.1 ,0.1)
# file_path = "C:\Users\chenyx\Desktop\NewDataSet\%s" % (0.5)
# url = file_path + '\data_test.txt'
# with codecs.open(url, "a", "utf-8") as f:
#     f.writelines(string)
