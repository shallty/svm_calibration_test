# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:34:59 2018

@author: H.T
"""

#
# 市场实际价格与MCS模拟价格差值函数
# price_dif.py
#
import numpy as np

from .stochastic_volatility_model_msc import StoVolaMoMsc


class CalibrationIns(object):
    ''' 参数校准工具类。
    
    Methods
    =======
    add_underlying : pandas.Series
        向容器中添加标的资产市场价格数据
    add_volatility : pandas.Series
        向容器中添加标的资产历史波动率数据
    add_strike_price : pandas.Series
        向容器中添加期权行权价格数据
    add_startdate : pandas.Series
        向容器中添加期权合约市场数据获取日期
    add_enddate : pandas.Series
        向容器中添加期权合约到期日
    add_rate : pandas.Series
        向容器中添加市场实际无风险一年期利率（shibor）
    add_mar_price : pandas.Series
        向容器中添加期权合约市场价格
    get_dif :
        取得不同参数下模拟数据与市场实际价格均方误差
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
    
    def get_dif(self, p):
        dif_t = []
        for i in range(len(self.mar_price)):
            dif = (self.mar_price[i] - StoVolaMoMsc(self.S0[i], self.r[i],
                   self.V0[i], p[0], p[1], p[2], p[3], self.strike_price[i], 
                   self.startdate[i], self.enddate[i]).get_option_price(
                           fixseed=True)[0]) ** 2
            dif_t.append(dif)
        z = np.mean(dif_t)
        print('%8.3f, %8.3f, %8.3f, %8.3f; outcome=%8.6f' % (p[0], p[1], p[2], 
                                                             p[3], z))
        return z