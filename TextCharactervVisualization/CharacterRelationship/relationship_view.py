# -*- coding: utf-8 -*-
from __future__ import print_function

"""
Created on 2017/10/15 19:24

@file: relationship_view.py
@author: Qingyu Mao
"""
import jieba
import codecs
from collections import defaultdict

TEXT_PATH = '../jsjs.txt'  # 文本路径
DICT_PATH = 'person.txt'  # 人物字典路径
SYNONYMOUS_DICT_PATH = 'synonymous_dict.txt'  # 同义词路径
SAVE_NODE_PATH = 'node.csv'
SAVE_EDGE_PATH = 'edge.csv'


class RelationshipView:
    def __init__(self, text_path, dict_path, synonymous_dict_path):
        self._text_path = text_path
        self._dict_path = dict_path
        self._synonymous_dict_path = synonymous_dict_path
        '''
        person_counter是一个计数器，用来统计人物出现的次数。{'a':1,'b':2}
        person_per_paragraph每段文字中出现的人物[['a','b'],[]]
        relationships保存的是人物间的关系。key为人物A，value为字典，包含人物B和权值。
        '''
        self._person_counter = defaultdict(int)
        self._person_per_paragraph = []
        self._relationships = {}
        self._synonymous_dict = {}

    def generate(self):
        self.count_person()
        self.calc_relationship()
        self.save_node_and_edge()

    def synonymous_names(self):
        '''
        获取同义名字典
        :return:
        '''
        with codecs.open(self._synonymous_dict_path, 'r', 'utf-8') as f:
            lines = f.read().split('\r\n')
        for l in lines:
            self._synonymous_dict[l.split(' ')[0]] = l.split(' ')[1]
        return self._synonymous_dict

    def get_clean_paragraphs(self):
        '''
        以段为单位分割全文
        :return:
        '''
        with codecs.open(self._text_path, 'r', 'utf-8') as f:
            paragraphs = f.read().split('\r\n\r\n')
        return paragraphs

    def count_person(self):
        '''
        统计人物出场次数，添加每段的人物
        :return:
        '''
        paragraphs = self.get_clean_paragraphs()
        synonymous = self.synonymous_names()
        print('start process node')
        with codecs.open(self._dict_path, 'r', 'utf-8') as f:
            name_list = f.read().split(' 10 nr\r\n')  # 获取干净的name_list
        for p in paragraphs:
            jieba.load_userdict(self._dict_path)
            # 分词，为每一段初始化新字典
            poss = jieba.cut(p)
            self._person_per_paragraph.append([])
            for w in poss:
                # 判断是否在姓名字典以及同义词区分
                if w not in name_list:
                    continue
                if synonymous.get(w):
                    w = synonymous[w]
                # 往每段中添加人物
                self._person_per_paragraph[-1].append(w)
                # 初始化人物关系，计数
                if self._person_counter.get(w) is None:
                    self._relationships[w] = {}
                self._person_counter[w] += 1
        return self._person_counter

    def calc_relationship(self):
        '''
        统计人物关系权值
        :return:
        '''
        print("start to process edge")
        for p in self._person_per_paragraph:
            for name1 in p:
                for name2 in p:
                    if name1 == name2:
                        continue
                    if self._relationships[name1].get(name2) is None:
                        self._relationships[name1][name2] = 1
                    else:
                        self._relationships[name1][name2] += 1
        return self._relationships

    def save_node_and_edge(self):
        '''
        根据dephi格式保存为csv
        :return:
        '''
        with codecs.open(SAVE_NODE_PATH, "a+", "utf-8") as f:
            f.write("Id,Label,Weight\r\n")
            for name, times in self._person_counter.items():
                f.write(name + "," + name + "," + str(times) + "\r\n")

        with codecs.open(SAVE_EDGE_PATH, "a+", "utf-8") as f:
            f.write("Source,Target,Weight\r\n")
            for name, edges in self._relationships.items():
                for v, w in edges.items():
                    if w > 3:
                        f.write(name + "," + v + "," + str(w) + "\r\n")
        print('save file successful!')


if __name__ == '__main__':
    v = RelationshipView(TEXT_PATH, DICT_PATH, SYNONYMOUS_DICT_PATH)
    v.generate()
