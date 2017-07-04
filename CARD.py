# -*- coding: utf-8 -*-
# __author__ = "静看沉浮"
# from math import *

# from multiprocessing import Process # 多线程
# import os # 多线程
# import pickle # 序列号读写
# import json # JSON格式支持
# import os # 文件读写
# from io import StringIO # 字符流数据读写
# from io import BytesIO # 二进制流数据读写
# import unittest # 单元测试
# import logging # 调试日志
# from enum import Enum #使用枚举类
# from functools import reduce
# from datetime import datetime
# import base64 #进行base64的编解码
# import hashlib #哈希计算库
import collections
Card = collections.namedtuple('Card', ['rank', 'suit'])
class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
    def __len__(self):
        return len(self._cards)
    def __getitem__(self, position):
        return self._cards[position]
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]
if __name__ == '__main__':
    deck = FrenchDeck()
    from random import choice
    choice(deck)
    for card in reversed(deck):
        print(card)
    for card in sorted(deck, key=spades_high):#将deck的元素逐个放入spades_high里面计算
        print(card)