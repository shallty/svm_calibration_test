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
import numpy.random as npr

from .get_workday import get_workday

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
        self.rho = rho
        self.K = K
        self.M = get_workday(startdate, enddate)
        self.dt = 1 / 252
        self.I = 100000
    
    def get_random(self):
        ''' 取得两个具有相关性的随机数矩阵。'''
        # 两个随机变量的相关系数矩阵
        corr_mat = np.array([[1, self.rho], [self.rho, 1]])
        cholesky_mat = np.linalg.cholesky(corr_mat)  # 进行cholesky变换
        ran_mat = npr.standard_normal((2, self.M, self.I))  # 生成随机数
        # 应用方差缩减
        ran_mat[0] = (ran_mat[0] - np.mean(ran_mat[0])) / np.std(ran_mat[0])
        ran_mat[1] = (ran_mat[1] - np.mean(ran_mat[1])) / np.std(ran_mat[1])
        for t in range(self.M):
            ran_mat[t] = np.dot(cholesky_mat, ran_mat[:, t, :])
        return ran_mat
    
    def get_option_price(self):
        ''' 产生期权价格。'''
        dt = 1 / 252
        opl = [] # 用于储存每一次模拟的期权价格
        for z in range(1000):
            V = np.zeros((self.M + 1, self.I))
            S = np.zeros((self.M + 1, self.I))
            S[0] = self.S0
            V[0] = self.V0
            for t in range(self.M):
                ran = self.get_random()[:, t, :]
                V[t + 1] = (V[t] + (self.kappa_v * (self.theta_v - V[t]) * dt + 
                 self.sigma_v * np.sqrt(V[t]) * np.sqrt[dt] * ran[1]))
                S[t + 1] = S[t] * np.exp((self.r - 0.5 * V[t]) *dt +
                 V[t] * np.sqrt(dt) * ran[0])
            op = (np.exp(-self.r * dt * self.M) * 
                  np.sum(np.maximum(S[-1] - self.K, 0)) / self.I)
            opl.append(op)
        return np.mean(opl)