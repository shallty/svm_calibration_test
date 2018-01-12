# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 10:50:39 2018

@author: H.T
"""

#
# 构造能生成具有相关性的随机数矩阵
# gen_random.py
#
import numpy as np
import numpy.random as npr

def gen_2d_corr_random(rho, M, I):
    ''' 构造相关性矩阵。
    
    Parameters
    ==========
    rho : float
        随机变量的相关性系数
    
    Returns
    =======
    ran_mat : ndarray
        具有相关性的矩阵
    '''
    corr_mat = np.array([[1, rho], [rho, 1]])
    cholesky_mat = np.linalg.cholesky(corr_mat)
    ran_mat = npr.standard_normal((2, M, I))
    for t in range(M):
        ran_mat[:, t, :] = np.dot(cholesky_mat, ran_mat[:, t, :])
    return ran_mat