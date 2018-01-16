# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:51:35 2018

@author: H.T
"""

#
# 市场数据容器
# market_environment.py
#


class market_environment(object):
    ''' 构造市场数据容器，让所有与校准有关的市场数据皆存储与容器中
    同时可以从容器中取得
    
    Methods
    =======
    get_** : 
        取得相应的实际市场数据
    add_** :
        向容器中添加相应的市场数据  
    '''
    
    def __init__(self):
        self.S0 = []
        self.V0 = []
        self.strike_price = []
        self.startdate = []
        self.enddate = []
        self.r = []
        self.mar_price = []
    
    def add_underlying(self, li):
        for i in range(len(li)):
            self.S0.append(li[i])
    
    def add_volatility(self, li):
        for i in range(len(li)):
            self.V0.append(li[i])
    
    def add_strike_price(self, li):
        for i in range(len(li)):
            self.strike_price.append(li[i])
    
    def add_startdate(self, li):
        for i in range(len(li)):
            self.startdate.append(li[i])
    
    def add_enddate(self, li):
        for i in range(len(li)):
            self.enddate.append(li[i])
    
    def add_rate(self, li):
        for i in range(len(li)):
            self.r.append(li[i])
    
    def add_mar_price(self, li):
        for i in range(len(li)):
            self.mar_price.append(li[i])
    
    def get_underlying(self):
        return self.S0
    
    def get_volatility(self):
        return self.V0
    
    def get_strike_price(self):
        return self.add_strike_price
    
    def get_startdate(self):
        return self.startdate
    
    def get_enddate(self):
        return self.enddate
    
    def get_rate(self):
        return self.r
    
    def get_mar_price(self):
        return self.mar_price