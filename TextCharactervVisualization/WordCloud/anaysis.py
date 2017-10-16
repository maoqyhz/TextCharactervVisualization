# -*- coding: utf-8 -*-
"""
Created on 2017/9/12 19:43

@file: anaysis.py
@author: Qingyu Mao
"""
from __future__ import print_function

import jieba.analyse
import matplotlib.pyplot as plt
from wordcloud import WordCloud

jieba.load_userdict("namedict.txt")

# 设置相关的文件路径
bg_image_path = "pic/image2.jpg"
text_path = '../jsjs.txt'
font_path = 'msyh.ttf'
stopwords_path = 'stopword.txt'


def clean_using_stopword(text):
    """
    去除停顿词，利用常见停顿词表+自建词库
    :param text:
    :return:
    """
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/".join(seg_list)
    with open(stopwords_path) as f_stop:
        f_stop_text = f_stop.read()
        f_stop_text = unicode(f_stop_text, 'utf-8')
    f_stop_seg_list = f_stop_text.split('\n')
    for myword in liststr.split('/'):  # 去除停顿词，生成新文档
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)
    return ''.join(mywordlist)


def preprocessing():
    """
    文本预处理
    :return:
    """
    with open(text_path) as f:
        content = f.read()
    return clean_using_stopword(content)
    return content


def extract_keywords():
    """
    利用jieba来进行中文分词。
    analyse.extract_tags采用TF-IDF算法进行关键词的提取。
    :return:
    """
    # 抽取1000个关键词，带权重，后面需要根据权重来生成词云
    allow_pos = ('nr',)  # 词性
    tags = jieba.analyse.extract_tags(preprocessing(), 1500, withWeight=True)
    keywords = dict()
    for i in tags:
        print("%s---%f" % (i[0], i[1]))
        keywords[i[0]] = i[1]
    return keywords


def draw_wordcloud():
    """
    生成词云。1.配置WordCloud。2.plt进行显示
    :return:
    """
    back_coloring = plt.imread(bg_image_path)  # 设置背景图片
    # 设置词云属性
    wc = WordCloud(font_path=font_path,  # 设置字体
                   background_color="white",  # 背景颜色
                   max_words=2000,  # 词云显示的最大词数
                   mask=back_coloring,  # 设置背景图片
                   )

    # 根据频率生成词云
    wc.generate_from_frequencies(extract_keywords())
    # 显示图片
    plt.figure()
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    # 保存到本地
    wc.to_file("wordcloud.jpg")


if __name__ == '__main__':
    draw_wordcloud()
