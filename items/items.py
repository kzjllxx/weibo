# -*- coding: utf-8 -*-
#-------------------------
#   版本：1.0
#   日期：2017年4月20日20:43:35
#   作者：kk
#-------------------------
from tools import wordstools

#修改目标：加入对表情的识别
def cal_implicit_degree(sentence):
    cutList = wordstools.cut_content(sentence,True)

    # 名词 形容词 介词 代词 动词 副词 感叹词
    noun, adj, prep, pron, verb, adv, int = 0, 0, 0, 0, 0, 0, 0
    total,f_score = 0.0,50
    for word in cutList:
        # print word.word + " --1"
        total += 1
        if word.flag == "n":
            noun += 1
        elif word.flag == "a":
            adj += 1
        elif word.flag == "p":
            prep += 1
        elif word.flag == "r":
            pron += 1
        elif word.flag == "v":
            verb += 1
        elif word.flag == "d":
            adv += 1
        elif word.flag == "e":
            int += 1
    if total != 0:
        f_score = 0.5 * (((noun + adj + prep) - (pron + verb + adv + int)) / total + 100)
    return float(f_score)

class NominalItem(object):
    # x = 0
    # n = 0
    # v = 0
    # m = 0
    # r = 0
    # d = 0
    # uj = 0
    # eng = 0
    # a = 0
    # nr = 0
    # p = 0
    # c = 0
    # ns = 0
    # ul = 0
    # t = 0
    # vn = 0
    # f = 0
    # y = 0
    # l = 0
    # nz = 0
    # q = 0
    # zg = 0
    # i = 0
    # b = 0
    # o = 0
    # nrt = 0
    # ng = 0
    # s = 0
    # z = 0
    # j = 0
    # u = 0
    # e = 0
    # ad = 0
    # uz = 0
    # k = 0
    # ug = 0
    # df = 0
    # ud = 0
    # vg = 0
    # nt = 0
    # ag = 0
    # an = 0
    # g = 0
    # uv = 0
    # mq = 0
    # tg = 0
    # nrfg = 0
    # yg = 0
    # vd = 0
    # rz = 0
    # h = 0
    # vq = 0
    # rr = 0
    # dg = 0
    # vi = 0
    # rg = 0
    # mg = 0

    def identify_nominal(self, word_flag):
        pass
    #判断含糊程度

