# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 15:35:37 2018

@author: H.T
"""

#
# 随机波动率模型蒙特卡洛模拟期权定价
# stochastic_volatility_model_msc.py
#
import numpy as np

from .get_workday import get_workday
from .gen_random import gen_2d_corr_random

class StoVolaMoMsc(object):
    ''' 随机波动率模型期权定价。
    
    Parameters
    ==========
    S0 : float
        标的资产初始价格
    r : float
        无风险利率
    V0 : float
        随机波动率初始数值
    kappa_v : float
        均值回复因子
    theta_v : float
        长期均值因子
    sigma_v : float
        波动率扩散项
    rho : float
        随机波动率和标的资产的相关系数
    K : float
        行权价格
    startdate : str
        开始日
    enddate : str
        到期日
    
    Returns
    =======
    op : float
        期权价格
    '''
    def __init__(self, S0, r, V0, kappa_v, theta_v, sigma_v, 
                 rho, K, startdate, enddate):
        self.S0 = S0
        self.r = r
        self.V0 = V0
        self.kappa_v = kappa_v
        self.theta_v = theta_v
        self.sigma_v = sigma_v
        # 直接对相关系数矩阵进行cholesky变换
        self.rho = rho
        self.K = K
        self.M = get_workday(startdate, enddate)
        self.dt = 1 / 252
        self.I = 100000
    
    def get_underlying(self):
        ''' 构建标的资产的价格变动函数。'''
        V = np.zeros((self.M + 1, self.I))
        S = np.zeros_like(V)
        V[0] = self.V0
        S[0] = self.S0
        ran = gen_2d_corr_random(self.rho, self.M, self.I)
        for t in range(self.M):
            V[t + 1] = (V[t] + (self.kappa_v * (self.theta_v - V[t]) * self.dt 
             + self.sigma_v * np.sqrt(V[t]) * np.sqrt(self.dt) * ran[1, t, :]))
            S[t + 1] = S[t] * np.exp((self.r - 0.5 * V[t]) * self.dt + 
             V[t] * np.sqrt(self.dt) * ran[0, t, :])
        return S
    
    def get_option_price(self, mul=False):
        ''' 产生期权价格。
        
        Parameters
        ==========
        mul : bool
            是否进行多次循环
            
        Returns
        =======
        option_price_describe_list : float
            期权价格
        '''
        opl = []  # 用于储存每一次模拟的期权价格
        if mul:
            for z in range(1000):
                S = self.get_underlying()
                op = (np.exp(-self.r * self.dt * self.M) * 
                      np.sum(np.maximum(S[-1] - self.K, 0)) / self.I)
                opl.append(op)
        else:
            for z in range(10):
                S = self.get_underlying()
                op = (np.exp(-self.r * self.dt * self.M) * 
                      np.sum(np.maximum(S[-1] - self.K, 0)) / self.I)
                opl.append(op)
        option_price_describe_list =  np.round([np.mean(opl), np.std(opl), 
                                                np.max(opl), np.min(opl)], 6)
        return option_price_describe_list