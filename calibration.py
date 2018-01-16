# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 10:32:44 2018

@author: H.T
"""

# 
# 校准函数
# calibration.py
#
import scipy.optimize as spo

class Calibrate(object):
    ''' 构造终极校准类。
    
    Parameters
    ==========
    price_dif_class : 
        含有市场实际价格信息的价差类
    
    Methods
    =======
    loc_fmin : 
        返回局部最小值
    opti_param : 
        返回最优参数
    '''
    def __init__(self, price_dif_class):
        self.dif_class = price_dif_class
        
    def loc_fmin(self):
        locmin = spo.brute(self.dif_class.get_dif, ((0, 5.1, 0.5), 
                                                    (0, 1.1, 0.1), 
                                                    (0, 1.1, 0.1),
                                                    (-1, 1.1, 0.2)), finish=None)
        return locmin
    
    def opti_param(self, initial_list):
        globalmin = spo.minimize(self.dif_class.get_dif, initial_list, 
                                 method='BFGS')
        if globalmin.success:
            print('参数校准最优化成功！')
            print('最优均方误差：%8.9f' % globalmin.fun)
            print('kappa_v: %8.9f' % globalmin.x[0])
            print('theta_v: %8.9f' % globalmin.x[1])
            print('sigma_v: %8.9f' % globalmin.x[2])
            print('rho: %8.9f' % globalmin.x[3])
            return globalmin.x
        else:
            print('参数校准失败，请重新设定起始参数！')
            print(globalmin.message)
            print('终止校准均方误差：%8.9f' % globalmin.fun)
            print('建议起始参数：')
            print('kappa_v: %8.9f' % globalmin.x[0])
            print('theta_v: %8.9f' % globalmin.x[1])
            print('sigma_v: %8.9f' % globalmin.x[2])
            print('rho: %8.9f' % globalmin.x[3])
            return globalmin.x